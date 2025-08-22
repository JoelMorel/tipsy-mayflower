let map, heatmap;

window.initMap = function () {
  const center = getCenter();
  map = new google.maps.Map(document.getElementById("map"), {
    center: center,
    mapTypeId: "roadmap",
    zoom: 12,
  });
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: getPoints(),
    map: map,
  });
};

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  const gradient = [
    "rgba(0, 255, 255, 0)",
    "rgba(0, 255, 255, 1)",
    "rgba(0, 191, 255, 1)",
    "rgba(0, 127, 255, 1)",
    "rgba(0, 63, 255, 1)",
    "rgba(0, 0, 255, 1)",
    "rgba(0, 0, 223, 1)",
    "rgba(0, 0, 191, 1)",
    "rgba(0, 0, 159, 1)",
    "rgba(0, 0, 127, 1)",
    "rgba(63, 0, 91, 1)",
    "rgba(127, 0, 63, 1)",
    "rgba(191, 0, 31, 1)",
    "rgba(255, 0, 0, 1)",
  ];
  heatmap.set("gradient", heatmap.get("gradient") ? null : gradient);
}

function changeRadius() {
  heatmap.set("radius", heatmap.get("radius") ? null : 20);
}

function changeOpacity() {
  heatmap.set("opacity", heatmap.get("opacity") ? null : 0.2);
}

function getPoints() {
  const points = Array.isArray(window.HEATMAP_POINTS)
    ? window.HEATMAP_POINTS
    : [];
  return points.map(function (p) {
    return {
      location: new google.maps.LatLng(p.lat, p.lng),
      weight: typeof p.weight === "number" ? p.weight / 100 : 1,
    };
  });
}

function getCenter() {
  if (
    window.HEATMAP_CENTER &&
    typeof window.HEATMAP_CENTER.lat === "number" &&
    typeof window.HEATMAP_CENTER.lng === "number"
  ) {
    return window.HEATMAP_CENTER;
  }
  return { lat: 40.7128, lng: -74.006 };
}
