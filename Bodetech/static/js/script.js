// Función para mostrar u ocultar los barriles por sector
function toggleBarriles(sectorId) {
    const barriles = document.getElementById(sectorId);
    
    // Toggle entre la clase 'activo' para mostrar u ocultar los barriles
    barriles.classList.toggle("activo");
}

// Función para mostrar u ocultar los datos de cada barril
function toggleDatos(barrilElement) {
    // Buscar si ya existe el contenedor de datos dentro del barril
    let datos = barrilElement.querySelector('.datos');
    
    // Si no existe, lo creamos
    if (!datos) {
        // Crear el contenedor de datos
        datos = document.createElement('div');
        datos.classList.add('datos');
        
        // Generar datos aleatorios
        const ph = (Math.random() * (7 - 3) + 3).toFixed(2); // Genera pH entre 3 y 7
        const temperatura = (Math.random() * (30 - 10) + 10).toFixed(1); // Temperatura entre 10 y 30°C
        const bebidas = ['Vino Tinto', 'Vino Blanco', 'Espumoso', 'Vino Rosado'];
        const bebida = bebidas[Math.floor(Math.random() * bebidas.length)];

        // Insertar los datos generados en el contenedor
        datos.innerHTML = `
            <p><strong>pH:</strong> ${ph}</p>
            <p><strong>Temperatura:</strong> ${temperatura} °C</p>
            <p><strong>Tipo de bebida:</strong> ${bebida}</p>
        `;
        
        // Añadir el contenedor de datos al barril
        barrilElement.appendChild(datos);
    } else {
        // Si ya existe el contenedor de datos, lo ocultamos o mostramos
        datos.style.display = datos.style.display === "block" ? "none" : "block";
    }
}








// Función para mostrar/ocultar tareas
function toggleTareas() {
    var tareas = document.getElementById("tareas");
    tareas.classList.toggle("activo");
}

// Función para mostrar/ocultar el formulario de agregar tarea
function toggleAgregarTarea() {
    var agregarTarea = document.getElementById("agregarTarea");
    agregarTarea.classList.toggle("activo");
}
