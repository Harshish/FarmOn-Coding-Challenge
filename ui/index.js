mapboxgl.accessToken =
  "pk.eyJ1Ijoic2NocmFtZXIiLCJhIjoiZE1xaHJ0VSJ9.fWza13i01BBb7o7VjFu6hA";
// Holds mousedown state for events. if this
// flag is active, we move the point on `mousemove`.
var isDragging;

// Is the cursor over a point? if this
// flag is active, we listen for a mousedown event.
var isCursorOverPoint;
let activeFeature;

var coordinates = document.getElementById("coordinates");
var map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v9",
  center: [5, 52],
  zoom: 6,
});

var canvas = map.getCanvasContainer();

var geojson = null;

function mouseDown() {
  if (!isCursorOverPoint) return;

  isDragging = true;

  // Set a cursor indicator
  canvas.style.cursor = "grab";

  // Mouse events
  map.on("mousemove", onMove);
  map.once("mouseup", onUp);
}

function onMove(e) {
  if (!isDragging) return;

  // Set a UI indicator for dragging.
  canvas.style.cursor = "grabbing";
  if (geojson === null) return;

  // Update the Point feature in `geojson` coordinates
  // and call setData to the source layer `point` on it.
  geojson.features[activeFeature.properties.position].geometry.coordinates = [
    e.lngLat.lng,
    e.lngLat.lat,
  ];

  map.getSource("points-data").setData(geojson);
  //console.log("DataSource:",map.getSource('points-data'));
  //console.log("Layer:", map.getLayer("point"));
}

function onUp(e) {
  if (!isDragging) return;

  // Print the coordinates of where the point had
  // finished being dragged to on the map.
  coordinates.style.display = "block";
  coordinates.innerHTML =
    "Longitude: " + e.lngLat.lng + "<br />Latitude: " + e.lngLat.lat;
  canvas.style.cursor = "";
  isDragging = false;

  // Unbind mouse events
  map.off("mousemove", onMove);
}

map.on("load", function () {
  // Add a single point to the map
  map.addSource("points-data", {
    type: "geojson",
    data: geojson,
  });

  map.addLayer({
    id: "point",
    type: "circle",
    source: "points-data",
    paint: {
      "circle-radius": 10,
      "circle-color": "#3887be",
    },
  });

  // When the cursor enters a feature in the point layer, prepare for dragging.
  map.on("mouseenter", "point", function (e, a, c) {
    map.setPaintProperty("point", "circle-color", "#3bb2d0");
    canvas.style.cursor = "move";
    isCursorOverPoint = true;
    map.dragPan.disable();
    activeFeature = e.features[0];
    console.log(e, activeFeature);
  });

  map.on("mouseleave", "point", function () {
    map.setPaintProperty("point", "circle-color", "#3887be");
    canvas.style.cursor = "";
    isCursorOverPoint = false;
    map.dragPan.enable();
  });

  map.on("mousedown", mouseDown);
});

function handleFindClick() {
  var longitude = document.getElementById("longitude").value;
  var latitude = document.getElementById("latitude").value;
  var crs = document.getElementById("crs").value;
  url = `http://localhost:8080/parcels/find_parcel_by_location?latitude=${latitude}&longitude=${longitude}&crs=${crs}`;

  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let field = [...data["centroid"]["coordinates"]];
      let soc = data["soc"];
      geojson = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            properties: {
              SOC: soc,
            },
            geometry: {
              type: "Point",
              coordinates: field,
            },
          },
        ],
      };
      console.log(geojson);

      map.getSource("points-data").setData(geojson);

      var socContent = document.getElementById("soc-content");
      socContent.innerHTML = soc + " g/kg";
    });

  //console.log("DataSource:",map.getSource('points-data'));
  //console.log("Layer:", map.getLayer("point"));
}
