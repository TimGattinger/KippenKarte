<!DOCTYPE html>
<html>
<head>
    <title>Map App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='leaflet/leaflet.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="{{ url_for('static', filename='leaflet/leaflet.js') }}"></script>
</head>
<body>
    <h1>Map App - Markers</h1>
    <div id="map" style="width: 800px; height: 600px;"></div>
    <script>
        var map = L.map('map').setView([54.323293, 10.122765], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);

        // Add existing markers
        {% for marker in markers %}
            L.marker([{{ marker.lat }}, {{ marker.lon }}], {icon: L.divIcon({className: 'leaflet-div-icon', html: '<i class="fas fa-map-pin"></i>'})})
                .bindPopup('{{ marker.label }}')
                .addTo(map);
        {% endfor %}

        map.on('click', function(e) {
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;
            var label = prompt('Enter a label for this marker:');
            
            if (label !== null && label.trim() !== '') {
                var marker = L.marker([lat, lon], {icon: L.divIcon({className: 'leaflet-div-icon', html: '<i class="fas fa-map-pin"></i>'})})
                    .bindPopup(label)
                    .addTo(map);

                // Send marker data to the server
                fetch('/add_marker', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `lat=${lat}&lon=${lon}&label=${encodeURIComponent(label)}`,
                });
            }
        });
    </script>
</body>
</html>


