async function showSidebar(embalseId) {
    const sidebar = document.getElementById('sidebar');

    // Si la barra lateral ya está visible, ocultarla
    if (sidebar.classList.contains('visible')) {
        sidebar.style.left = '-300px'; // Mover a la posición oculta
        setTimeout(() => {
            sidebar.style.display = 'none'; // Ocultar completamente
            sidebar.classList.remove('visible'); // Quitar clase visible
        }, 500);
        return;
    }

    // Mostrar la barra lateral inmediatamente
    sidebar.style.display = 'block';
    setTimeout(() => {
        sidebar.style.left = '0';
        sidebar.classList.add('visible');
    }, 20);

    // Construir la URL para llamar a la API
    const apiUrl = `api/analytics/load_data_id?id=${embalseId}`;

    // Llamar a la API para obtener los datos del embalse
    try {
        const response = await fetch(apiUrl);

        // Verificar si la respuesta es válida
        if (!response.ok) {
            throw new Error('Error en la respuesta de la API');
        }

        const data = await response.json();

        // Actualizar la información en la barra lateral
        document.getElementById('embalse-nombre').textContent = `Embalse ID: ${embalseId}`;
        document.getElementById('embalse-ubicacion').textContent = "Ubicación del Embalse";
        document.getElementById('embalse-capacidad').textContent = "Capacidad: N/A";

        // Extraer datos para la gráfica
        const fechas = data.map(entry => entry.FECHA);
        const nivelesAgua = data.map(entry => entry.AGUA_ACTUAL);

        // Mostrar la gráfica
        mostrarGrafica(fechas, nivelesAgua);

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
