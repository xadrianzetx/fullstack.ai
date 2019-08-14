const handler = new MapEventHandler();

function onMarkerClick(data) {
    
    if (!handler.isStartPointSet && !handler.isPredicted) {
        // new starting point
        handler.setStartPoint(data);
        var popularStations = data.target.options.popular
        var startCoords = data['latlng'];

        for (key in popularStations) {
            // get top 3 most popular endpoints from current station
            var popularCoords = popularStations[key];
            var latlng = [
                [startCoords['lat'], startCoords['lng']], 
                [popularCoords['latitude'], popularCoords['longitude']]
            ];
            
            // TODO customize those, ok?
            L.polyline(latlng).addTo(map);
        }

    } else if (handler.isStartPointSet && !handler.isPredicted) {
        // when starting point has been set
        // set end point and await prediction
        handler.setEndPoint(data).then(function (datum) {
            // clear most popular routes and
            // add polyline for selected one
            clearAllPolylines();
            var startCoords = handler.startStationCoords;
            var currentCoords = data['latlng'];
            var latlng = [
                [startCoords['lat'], startCoords['lng']],
                [currentCoords['lat'], currentCoords['lng']]
            ];

            // TODO again, customize
            L.polyline(latlng).addTo(map);
            console.log(datum['predicted']);
            // TODO this also should handle text updating
        });

    }
}

function onMapClick(data) {

    if (handler.isPredicted) {
        // prediction has been made reset map to original state
        handler.reset();
        clearAllPolylines();
        // TODO reset text

    } else {
        // reset without prediction on user call
        handler.startPointSet = false;
        clearAllPolylines();

    }
}

function clearAllPolylines() {
    // src https://stackoverflow.com/questions/14585688/clear-all-polylines-from-leaflet-map
    for(i in map._layers) {
        if(map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }
}

var map = L.map('map').setView([37.788850, -122.401967], 14);
map.on('click', onMapClick);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">\
        OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">\
        CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: config['mapboxApiKey']
}).addTo(map);

$.ajax({
    type: 'GET',
    url: '/get_stations',
    contentType: 'application/json',
    success: function(data) {
        for (var key in data) {
            // load all stations to map with id and metadata
            var station = data[key]
            var marker = L.marker(
                [station['latitude'], station['longitude']],
                {id: key, popular: data[key]['pop_dest']}
            );

            marker.addTo(map);
            marker.bindTooltip(station['name']);
            marker.on('click', onMarkerClick);
        }
    }
});
