let map;

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
        center: { lat: 40.4168, lng: -3.7038 }, // Centro en España
        zoom: 6,
    });

    // Cargar los datos desde el servidor y agregar los marcadores
    const items = await fetchItems();
    items.forEach(item => addMarker(item));
}

// Función para obtener datos desde el backend
async function fetchItems() {
    const response = await fetch('/api/analytics/load_data');
    const data = await response.json();
    return data;
}

// Función para agregar un marcador en el mapa
function addMarker(item) {
    const marker = new google.maps.Marker({
        position: { lat: item.lat, lng: item.lng },
        map: map,
        title: item.nombre,
    });

    // Evento para mostrar la barra lateral al hacer clic en el marcador
    marker.addListener("click", () => {
        showSidebar(item);
    });
}

initMap();