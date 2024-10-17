// Función para mostrar la barra lateral
async function showSidebar(embalseId) {
    const sidebar = document.getElementById('sidebar');

    // Si la barra lateral ya está visible, ocultarla
    if (sidebar.classList.contains('visible')) {
        sidebar.style.left = '-300px'; // Mover a la posición oculta
        setTimeout(() => {
            sidebar.style.display = 'none'; // Ocultar completamente
            sidebar.classList.remove('visible'); // Quitar clase visible
        }, 500); // Tiempo de la transición
        return; // Salir de la función
    }

    // Asegúrate de que embalseId sea un número válido
    if (typeof embalseId !== 'number' || isNaN(embalseId)) {
        console.error('ID de embalse no válido:', embalseId);
        return; // Salir de la función
    }

    // Construir la URL para llamar a la API con el ID del embalse
    const apiUrl = `api/analytics/load_data?id=${embalseId}`; // Cambia el ID según sea necesario

    // Llamar a la API para obtener los datos del embalse
    try {
        const response = await fetch(apiUrl);

        // Verificar si la respuesta es válida
        if (!response.ok) {
            throw new Error('Error en la respuesta de la API');
        }

        const data = await response.json();

        // Actualizar la información en la barra lateral
        document.getElementById('embalse-nombre').textContent = `Embalse ID: ${embalseId}`; // Puedes personalizar esto
        document.getElementById('embalse-ubicacion').textContent = "Ubicación del Embalse"; // Cambia según la respuesta de la API
        document.getElementById('embalse-capacidad').textContent = "Capacidad: N/A"; // Cambia según la respuesta de la API

        // Extraer datos para la gráfica
        const fechas = data.map(entry => entry.FECHA);
        const nivelesAgua = data.map(entry => entry.AGUA_ACTUAL);

        // Mostrar la gráfica
        mostrarGrafica(fechas, nivelesAgua); // Asegúrate de tener esta función definida

        // Mostrar la barra lateral
        sidebar.style.display = 'block'; // Mostrar
        setTimeout(() => {
            sidebar.style.left = '0'; // Mover a la posición visible
            sidebar.classList.add('visible'); // Añadir clase visible
        }, 20); // Pequeña pausa para permitir que el navegador registre el cambio de estilo

    } catch (error) {
        console.error('Error al obtener los datos del embalse:', error);
    }
}

function mostrarGrafica(fechas, nivelesAgua) {
    const ctx = document.getElementById('embalse-grafica').getContext('2d');
    
    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechas,
            datasets: [{
                label: 'Evolución del nivel de agua',
                data: nivelesAgua,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        },
        options: {
            scales: {
                x: { 
                    type: 'time',
                    time: {
                        unit: 'month'
                    }
                },
                y: { beginAtZero: true }
            }
        }
    });
}

// Añadir el evento al botón
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('.button');
    button.addEventListener('click', () => showSidebar(18)); // Llama a la función con un ID de embalse de ejemplo
});
