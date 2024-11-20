from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps

app = Flask(__name__, static_url_path='/static')
load_dotenv()

# Conectar a MySQL
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '12345')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Configuración de Flask-Login
app.secret_key = "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."

# Modelo de usuario
class User(UserMixin):
    def __init__(self, email, contraseña, is_admin=False):
        self.id = email
        self.email = email
        self.contraseña = contraseña
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(email):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT correo, contraseña, is_admin FROM usuarios WHERE correo = %s", (email,))
        user = cur.fetchone()
        if user:
            print(f"Usuario cargado: {user}")  # verifica los datos cargados
            return User(user[0], user[1], user[2])
    return None

# Decorador para restringir acceso de admin
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acceso denegado: solo el administrador puede acceder a esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT correo, contraseña, is_admin FROM usuarios WHERE correo = %s", (email,))
            user = cur.fetchone()
            if user:
                user_obj = User(user[0], user[1], user[2])
                print(f"Usuario encontrado: {user_obj.email}, is_admin: {user_obj.is_admin}") 
                if password == user_obj.contraseña:
                    login_user(user_obj)
                    flash('¡Inicio de sesión exitoso!', 'success')
                    if user_obj.is_admin:
                        return redirect(url_for('inicio')) 
                    else:
                        error = "No tienes permisos de administrador para acceder a esta página."
                else:
                    error = "Credenciales inválidas. Por favor, inténtalo de nuevo."
            else:
                error = "Usuario no encontrado en el sistema."
    
    return render_template('login.html', error=error)

# Ruta principal
@app.route('/')
def main():
    return redirect(url_for('login'))

#ruta despues de login
@app.route('/inicio')
@login_required
def inicio():
    return render_template ('index.html')

#ruta vacia para probar bug
@app.route('/historial_barriles')
def historial_barriles():
    return "Página de historial de barriles en desarrollo"

# Ruta de cierre de sesion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

# Leer datos de usuarios
@app.route('/usuarios')
@admin_required
def usuarios():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('SELECT nombre, apellido, correo, is_admin FROM usuarios')
            data = cur.fetchall()
        return render_template('index.html', usuarios=data)
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
        flash('Error al obtener los datos', 'error')
        return redirect(url_for('usuarios'))

# Cargar usuario
@app.route('/cargar_usuario', methods=['GET', 'POST'])
@admin_required
def cargar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        is_admin = request.form.get('is_admin', False)

        try:
            with mysql.connection.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuarios 
                    (nombre, apellido, correo, contraseña, is_admin) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nombre, apellido, correo, contraseña, is_admin))
                mysql.connection.commit()
            flash('Usuario cargado correctamente', 'success')
            return redirect(url_for('usuarios'))
        except Exception as e:
            print(f"Error al cargar usuario en la base de datos: {str(e)}")
            flash('Error al cargar usuario', 'error')

    return render_template('cargarUsuario.html')

# Editar usuario
@app.route('/editar_usuario/<correo>', methods=['GET', 'POST'])
@login_required
def editar_usuario(correo):
    try:
        if request.method == 'GET':
            with mysql.connection.cursor() as cur:
                cur.execute('SELECT nombre, apellido, correo, is_admin FROM usuarios WHERE correo = %s', (correo,))
                data = cur.fetchone()
            return render_template('editar_usuario.html', usuario=data)
        
        elif request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            nuevo_correo = request.form['correo']
            is_admin = request.form['is_admin']

            with mysql.connection.cursor() as cur:
                cur.execute("""
                    UPDATE usuarios
                    SET nombre = %s,
                        apellido = %s,
                        correo = %s,
                        is_admin = %s
                    WHERE correo = %s
                """, (nombre, apellido, nuevo_correo, is_admin, correo))
                mysql.connection.commit()

            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('usuarios'))

    except Exception as e:
        print(f"Error al editar usuario en la base de datos: {str(e)}")
        flash('Error al editar usuario', 'error')
        return redirect(url_for('usuarios'))


@app.route('/tareas')
@login_required
def tareas():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('SELECT id, nombre_tarea, encargado, fecha, completada FROM tareas')
            tareas = cur.fetchall() 
        return render_template('index.html', tareas=tareas)  
    except Exception as e:
        print(f"Error al obtener tareas: {e}")
        flash('Error al obtener tareas', 'error')
        return redirect(url_for('inicio'))


# Ruta para agregar tarea
@app.route('/agregar_tarea', methods=['POST'])
@login_required
def agregar_tarea():
    if 'nombre_tarea' in request.form and 'descripcion_tarea' in request.form and 'encargado' in request.form and 'fecha' in request.form:
        nombre_tarea = request.form['nombre_tarea']
        descripcion_tarea = request.form['descripcion_tarea']
        encargado = request.form['encargado']
        fecha = request.form['fecha']
        
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO tareas (nombre_tarea, descripcion_tarea, encargado, fecha, completada) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre_tarea, descripcion_tarea, encargado, fecha, False))  
                mysql.connection.commit()
            flash('Tarea agregada exitosamente!', 'success')
        except Exception as e:
            flash('Error al agregar la tarea', 'error')
            print(f"Error al agregar tarea: {e}")
    else:
        flash('Error: Datos incompletos', 'error')
        
    return redirect(url_for('tareas')) 

# Ruta para cambiar el estado de la tarea a completada
@app.route('/toggle_completada/<int:id>', methods=['PATCH'])
@login_required
def toggle_completada(id):
    try:
        with mysql.connection.cursor() as cur:

            cur.execute("SELECT completada FROM tareas WHERE id = %s", (id,))
            tarea = cur.fetchone()
            if tarea:
                nueva_estado = not tarea[0] 
                cur.execute("UPDATE tareas SET completada = %s WHERE id = %s", (nueva_estado, id))
                mysql.connection.commit()
                return {'completada': nueva_estado}
            else:
                return {'error': 'Tarea no encontrada'}, 404
    except Exception as e:
        print(f"Error al cambiar el estado de la tarea: {str(e)}")
        return {'error': 'Error al actualizar el estado'}, 500



# Iniciar el servidor
if __name__ == '__main__':
    app.run(port=9000, debug=True)
