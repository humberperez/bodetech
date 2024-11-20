document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const triggerArea = document.querySelector(".trigger-area");

    // Mostrar la barra lateral al pasar el mouse por el área de activación
    triggerArea.addEventListener("mouseenter", function () {
        sidebar.classList.add("open"); // Mostrar la barra
    });

    // Ocultar la barra lateral cuando el mouse salga de ella
    sidebar.addEventListener("mouseleave", function () {
        sidebar.classList.remove("open"); // Ocultar la barra
    });
});
