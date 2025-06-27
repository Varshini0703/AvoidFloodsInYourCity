document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([51.505, -0.09], 5);

    L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: 'Map data &copy; <a href="https://www.google.com/maps">Google Maps</a>'
    }).addTo(map);

    var marker;
    var geocoder = L.Control.Geocoder.nominatim();
    var placeInput = document.getElementById('placeInput');
    var suggestionsContainer = document.getElementById('suggestions');

    placeInput.addEventListener('input', function(e) {
        var query = placeInput.value;
        if (query) {
            geocoder.geocode(query, function(results) {
                suggestionsContainer.innerHTML = '';
                if (results && results.length > 0) {
                    results.forEach(function(result) {
                        var suggestionDiv = document.createElement('div');
                        suggestionDiv.textContent = result.name;
                        suggestionDiv.addEventListener('click', function() {
                            placeInput.value = result.name;
                            suggestionsContainer.innerHTML = '';
                            map.setView(result.center, 13);
                            if (marker) {
                                marker.setLatLng(result.center);
                            } else {
                                marker = L.marker(result.center).addTo(map);
                            }
                            marker.bindPopup(result.name).openPopup();
                        });
                        suggestionsContainer.appendChild(suggestionDiv);
                    });
                }
            });
        } else {
            suggestionsContainer.innerHTML = '';
        }
    });

    var precipitationLayer = L.tileLayer('https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=9b44d42714e481be282853dcd4ea3ed1', {
        attribution: 'Map data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
        opacity: 100
    });

    var temperatureLayer = L.tileLayer('https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=9b44d42714e481be282853dcd4ea3ed1', {
        attribution: 'Map data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
        opacity: 7
    });

    var pressureLayer = L.tileLayer('https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=9b44d42714e481be282853dcd4ea3ed1', {
        attribution: 'Map data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
        opacity: 7
    });

    var overlayMaps = {
        "Precipitation": precipitationLayer,
        "Temperature": temperatureLayer,
        "Pressure": pressureLayer
    };

    L.control.layers(null, overlayMaps, { collapsed: false }).addTo(map);
});