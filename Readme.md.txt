# Proyecto Malackaton

Este proyecto proporciona una interfaz web diseñada para interactuar con datos sobre embalses, incorporando diversas funcionalidades que permiten a los usuarios explorar y visualizar información relevante de manera intuitiva.

---

## Estructura General

### Cabecera (Head)
- **Configuración básica**: Incluye el título del documento, la codificación de caracteres y la referencia a un archivo de estilos CSS.
- **Icono de la página**: Se establece un icono personalizado para la interfaz.

### Cuerpo (Body)
#### Encabezado (Header)
- **Control deslizante**: Permite ajustar el radio de búsqueda.
- **Botón de filtros**: Un botón para aplicar criterios de búsqueda.
- **Formulario oculto**: Facilita la entrada de criterios de búsqueda (comunidad autónoma, eléctrica, agua y provincia).

#### Mapa
- Un elemento `<div>` que alberga un mapa interactivo, implementado con Google Maps.

#### Barra Lateral (Sidebar)
- Muestra información detallada sobre un embalse específico:
  - **Nombre**: Nombre del embalse.
  - **Ubicación**: Información sobre su ubicación geográfica.
  - **Capacidad**: Capacidad del embalse (actualmente N/A).
  - **Enlace a más detalles**: Proporciona acceso a información adicional.
- **Gráficos**: Un elemento `<canvas>` destinado a mostrar gráficos relacionados con los datos del embalse.

### Scripts
Se utilizan varias bibliotecas JavaScript:
- **FingerprintJS**: Para capturar y enviar un identificador de visitante al backend.
- **Chart.js**: Para crear gráficos visuales en el `<canvas>`.
- **Google Maps API**: Para gestionar la visualización del mapa.

---

## Funcionalidades Clave
- **Interactividad**: El control deslizante permite a los usuarios ajustar el radio de búsqueda en tiempo real.
- **Filtrado y Búsqueda**: Facilita la búsqueda de embalses según varios parámetros.
- **Visualización**: Muestra un mapa interactivo y detalles gráficos, facilitando una comprensión visual de la información.

---

## Resumen de Archivos JavaScript

### `map.js`
1. **Variables Iniciales**: 
   - Se declaran variables para el mapa, ubicación del usuario y posición central.
   - Inicializa `circle` y `radiusValue`.

2. **Control del Radio**: 
   - Se obtiene el control deslizante y se añade un evento para actualizar el radio del círculo en el mapa.

3. **Cálculo de Distancias**: 
   - Utiliza la fórmula del Haversine para determinar distancias entre puntos geográficos.

4. **Obtener Posición del Usuario**: 
   - Usa la API de geolocalización para centrar el mapa en la ubicación actual del usuario.

5. **Envío de Datos**: 
   - Envía la ubicación del usuario al servidor mediante un POST en formato JSON.

6. **Inicialización del Mapa**: 
   - Crea el mapa de Google Maps, marcadores y ajusta la vista.

---

### `home.js`
1. **Función `showSidebar(item)`**: 
   - Maneja la visualización de una barra lateral con detalles de un embalse.
   - Comprobaciones para mostrar u ocultar la barra lateral y realizar llamadas a la API.

2. **Llamada a la API**: 
   - Recupera datos específicos del embalse y actualiza la interfaz.

3. **Función `mostrarGrafica(fechas, nivelesAgua)`**: 
   - Crea y muestra gráficas de niveles de agua utilizando Chart.js.

---

## Consideraciones
- **Interactividad**: La barra lateral se muestra y oculta de forma animada, mejorando la experiencia del usuario.
- **Actualización Dinámica**: La aplicación utiliza `fetch` para obtener datos en tiempo real.
- **Visualización de Datos**: Chart.js facilita la comprensión de la evolución de los niveles de agua.

---

## Instalación
Para ejecutar el proyecto, sigue estos pasos:

1. Clona este repositorio:
   En bash:
   git clone https://github.com/vegonza/Malackaton.git