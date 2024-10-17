let map;
let latitud, longitud;
let centrallat = 40.4168;
let centrallong = -3.7038;
let circle;
let radiusValue = 100;

const radiusSlider = document.getElementById('radius-slider');
const radiusValueDisplay = document.getElementById('radius-value');

radiusSlider.addEventListener('input', function() {
  radiusValue = parseInt(this.value); // Get the radius from the slider
  radiusValueDisplay.textContent = radiusValue; // Update the displayed value
  if (circle) {
    circle.setRadius(radiusValue * 1000); // Update the circle's radius
    map.fitBounds(circle.getBounds());
  }
});

function calcularDistancia(lat1, lon1, lat2, lon2) {
  const radioTierra = 6371; // Earth's radius in kilometers
  const radLat1 = degToRad(lat1);
  const radLat2 = degToRad(lat2);
  const deltaLat = degToRad(lat2 - lat1);
  const deltaLon = degToRad(lon2 - lon1);

  const a =
    Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
    Math.cos(radLat1) *
      Math.cos(radLat2) *
      Math.sin(deltaLon / 2) *
      Math.sin(deltaLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distancia = radioTierra * c;

  return distancia;
}

function degToRad(grados) {
  return (grados * Math.PI) / 180;
}

function getPosition() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(resolve, () => {
        // If geolocation fails, resolve with default position
        resolve({ coords: { latitude: centrallat, longitude: centrallong } });
      });
    } else {
      // If geolocation is not supported, resolve with default position
      resolve({ coords: { latitude: centrallat, longitude: centrallong } });
    }
  });
}

async function post_loc(lat, long) {
  const data = { lat: lat, lng: long };
  
  try {
    const response = await fetch('/api/sql/embalses_cords', {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const items = await response.json(); // Assumes the response is a list of {lat, lng} objects
    console.log('Respuesta del servidor:', items);
    return items; // Return the list of items

  } catch (error) {
    console.error('Error:', error);
    return []; // Return an empty list if there’s an error
  }
}

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");   

  const mapOptions = {
    center: { lat: latitud, lng: longitud },
    zoom: 6,
    disableDefaultUI: true,  // Disables all default UI controls
    fullscreenControl: false,
    streetViewControl: false,
    mapTypeControl: false,
    styles: [  // Custom styles to remove specific map elements
        {
            featureType: "poi",  // Points of interest
            stylers: [{ visibility: "off" }]
        },
        {
            featureType: "transit",  // Transit routes and stations
            stylers: [{ visibility: "off" }]
        },
        {
            featureType: "road",  // Roads
            stylers: [{ visibility: "off" }]
        },
        {
            featureType: "administrative",  // Administrative boundaries
            stylers: [{ visibility: "off" }]
        },
        {
            featureType: "landscape.man_made",  // Man-made structures
            stylers: [{ visibility: "off" }]
        },
        {
            featureType: "poi.business",  // Businesses
            stylers: [{ visibility: "off" }]
        }
    ]
  };
  map = new Map(document.getElementById("map"), mapOptions);
  
  if (latitud !== centrallat || longitud !== centrallong) {
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
      radius: radiusValue * 1000, 
    });

    map.fitBounds(circle.getBounds());

    const items = await post_loc(latitud, longitud);

    items.forEach(item => {
      if (calcularDistancia(latitud, longitud, item.lat, item.lng) <= radiusValue) {
        addMarker(item);
      }
    });
    
  } else {
    const items = await fetchItems();
    items.forEach(item => addMarker(item));
  }
}

// Function to fetch items from the backend
async function fetchItems() {
  try {
    const response = await fetch('/api/analytics/load_data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching items:', error);
    return [];
  }
}

// Function to add a marker to the map
function addMarker(item) {
  const marker = new google.maps.Marker({
    position: { lat: item.lat, lng: item.lng },
    map: map,
    icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    title: item.nombre,
  });

  // Event to show the sidebar when clicking on the marker
  marker.addListener("click", () => {
    showSidebar(item);
  });
}

// Main function to get position and initialize map
(async function() {
  const position = await getPosition();
  latitud = position.coords.latitude;
  longitud = position.coords.longitude;

  radiusValueDisplay.textContent = radiusValue; // Initialize radius value display

  await initMap();
})();
