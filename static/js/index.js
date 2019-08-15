const handler = new MapEventHandler();

function onMarkerClick(data) {
    
    if (!handler.isStartPointSet && !handler.isPredicted) {
        // new starting point
        handler.setStartPoint(data);
        var popularStations = data['target']['options']['popular'];
        var keys = Object.keys(popularStations);
        var startCoords = data['latlng'];
        var startName = data['target']['options']['name'];

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

        $('.notice-current').html('<strong>Start</strong> ' + startName);
        $('.notice-current').toggle();

        for (i = 0; i <= 2; i++) {
            // toggle most popular stations
            var key = keys[i];
            var name = popularStations[key]['name'];
            $('.notice-popular-' + i).toggle();
            $('.notice-popular-' + i).html('<strong>Popular destination</strong> ' + name);
        }

    } else if (handler.isStartPointSet && !handler.isPredicted) {
        // set end point and await prediction
        handler.setEndPoint(data).then(function (datum) {
            clearAllPolylines();

            var startCoords = handler.startStationCoords;
            var currentCoords = data['latlng'];
            var latlng = [
                [startCoords['lat'], startCoords['lng']],
                [currentCoords['lat'], currentCoords['lng']]
            ];

            L.polyline(latlng).addTo(map);

            for (i = 0; i <= 2; i++) {
                // turn off most popular routes
                $('.notice-popular-' + i).toggle();
            }
            
            // parse time
            var min = parseInt(datum['predicted']);
            var sec = Math.round((datum['predicted'] - min) * 60);
            var total = min + ' minutes ' + sec + ' seconds'
            var endName = data['target']['options']['name'];
            
            // toggle notes with updated text
            $('.notice-predicted').html('<strong>Predicted trip time</strong> ' + total);
            $('.notice-end').html('<strong>End</strong> ' + endName);
            $('.notice-end').toggle();
            $('.notice-predicted').toggle();
        });

    }
}

function onMapClick(data) {

    if (handler.isPredicted && handler.isStartPointSet) {
        // prediction has been made reset map to original state
        handler.reset();
        clearAllPolylines();
        $('.notice-current').toggle();
        $('.notice-end').toggle();
        $('.notice-predicted').toggle();

    } else if (!handler.isPredicted && handler.isStartPointSet) {
        // reset without prediction on user call
        handler.startPointSet = false;
        clearAllPolylines();
        $('.notice-current').toggle();
        
        for (i = 0; i <= 2; i++) {
            $('.notice-popular-' + i).toggle();
        }

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
            // load all stations with id and metadata
            var station = data[key]
            var marker = L.marker(
                [station['latitude'], station['longitude']],
                {id: key, name: station['name'], popular: data[key]['pop_dest']}
            );

            marker.addTo(map);
            marker.bindTooltip(station['name']);
            marker.on('click', onMarkerClick);
        }
    }
});
