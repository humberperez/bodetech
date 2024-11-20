
// Función para mostrar/ocultar tareas
function toggleTareas() {
    var tareas = document.getElementById("tareas");
    tareas.classList.toggle("activo");
}

function toggleAgregarTarea() {
    var agregarTarea = document.querySelector(".agregar-tarea");
    agregarTarea.classList.toggle("activo"); // Alterna la clase "activo" que muestra u oculta el formulario
}

// Función para actualizar el estado de completada de la tarea
function toggleCompletada(id) {
    fetch(`/toggle_completada/${id}`, { method: 'PATCH' })
        .then(response => response.json())
        .then(data => {
            // Actualiza el estado de la tarea sin recargar la página
            const checkbox = document.querySelector(`[onclick="toggleCompletada(${id})"]`);
            checkbox.checked = data.completada;
        })
        .catch(error => console.error('Error:', error));
}
