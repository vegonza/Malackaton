let map;
let latitud,longitud

function getPos(position) {
    latitud=position.coords.latitude
    longitud=position.coords.longitude
  }
  
  if(!navigator.geolocation) {
    console.log('No se puede')
  } else {
    navigator.geolocation.getCurrentPosition(getPos)
  }

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
        center: { lat: 40.4168, lng: -3.7038 }, // Centro en España
        zoom: 6,
    });

    var radio = new google.maps.Circle({
        strokeColor: "blue",
        strokeOpacity: 0.9,
        strokeWeight: 2,
        fillColor: "blue",
        fillOpacity: 0.15,
        map: map,
        center: {
          lat: latitud,
          lng: longitud
        },
        radius: 1000 * 100
      });
    
    map.fitBounds(radio.getBounds());

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
        icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        title: item.nombre,
    });

    // Evento para mostrar la barra lateral al hacer clic en el marcador
    marker.addListener("click", () => {
        showSidebar(item);
    });
}

initMap();