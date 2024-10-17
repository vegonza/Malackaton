let map;
let latitud,longitud
let centrallat=40.4168
let centrallong=-3.7038
let circle; 
let radiusValue = 100;


const radiusSlider = document.getElementById('radius-slider');
const radiusValueDisplay = document.getElementById('radius-value');

radiusSlider.addEventListener('input', function() {
  radiusValue = parseInt(this.value); // Get the radius from the slider
  radiusValueDisplay.textContent = radiusValue; // Update the displayed value
  circle.setRadius(radiusValue*1000); // Update the circle's radius
  map.fitBounds(circle.getBounds());
});

function calcularDistancia(lat1, lon1, lat2, lon2) {
  // Radio de la Tierra en kilómetros
  const radioTierra = 6371;

  // Convertir las coordenadas de grados a radianes
  const radLat1 = degToRad(lat1);
  const radLat2 = degToRad(lat2);
  const deltaLat = degToRad(lat2 - lat1);
  const deltaLon = degToRad(lon2 - lon1);

  // Fórmula del Haversine
  const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
            Math.cos(radLat1) * Math.cos(radLat2) *
            Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  // Distancia en kilómetros
  const distancia = radioTierra * c;

  return distancia;
}

function degToRad(grados) {
  return grados * (Math.PI / 180);
}

function getPos(position) {
    latitud=position.coords.latitude
    longitud=position.coords.longitude
  }
  
if(!navigator.geolocation) {
  console.log('No se puede')
  latitud=centrallat
  longitud=centrallong
} else {
  navigator.geolocation.getCurrentPosition(getPos)
  console.log(latitud);
}

if(typeof latitud === 'undefined') {
  latitud=centrallat
  longitud=centrallong
}

async function post_loc(lat,long) {
  data={lat:lat,lng:long};
  fetch('/recibir_datos', {
      method: 'POST', // Método POST para enviar datos
      headers: {
          'Content-Type': 'application/json', // Indica que estamos enviando JSON
      },
      body: JSON.stringify(data) // Convertimos el objeto JS a JSON
  })
  .then(response => response.json())
  .then(data => {
      console.log('Respuesta del servidor:', data);
  })
  .catch((error) => {
      console.error('Error:', error);
  });  
}

post_loc(latitud,longitud)

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");   

    map = new Map(document.getElementById("map"), {
        center: { lat: latitud, lng: longitud }, // Centro en España
        zoom: 6,
    });

    // Cargar los datos desde el servidor y agregar los marcadores
    
    if(latitud !==centrallat) {
      const actual = new google.maps.Marker({
        position: { lat: latitud, lng: longitud },
        map: map,
        icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
        title: "Posición actual",
      });

        circle = new google.maps.Circle({
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
          radius: radiusValue*1000, 
        });
      
    
      map.fitBounds(circle.getBounds());
    
      items.forEach(item => {
        if (calcularDistancia(latitud,longitud,item.lat,item.lng)<=100) addMarker(item);
      });
      
    } else {
      items.forEach(item => addMarker(item));
    }
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