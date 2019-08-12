const handler = new MapEventHandler();

function onMarkerClick(data) {
    
    if (!handler.isStartPointSet && !handler.isPredicted) {
        // new starting point
        handler.setStartPoint(data);

    } else if (handler.isStartPointSet && !handler.isPredicted) {
        // when starting point has been set
        // set end point and call for prediction
        var predicted = handler.setEndPoint(data);
        console.log(predicted);
        // TODO this also should handle drawing
        // and text updating

    }
}

function onMapClick(data) {

    if (handler.isPredicted) {
        // prediction has been made reset map to ori state
        handler.reset();
        // TODO reset drawing and text

    } else {
        // reset without prediction on user call
        handler.startPointSet = false;

    }

}

var map = L.map('map').setView([37.788850, -122.401967], 14);
map.on('click', onMapClick);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: config['mapboxApiKey']
}).addTo(map);

// I hate js
$.ajax({
    type: 'GET',
    url: '/get_stations',
    contentType: 'application/json',
    success: function(data) {
        // load all stations to map
        for (var key in data) {
            var station = data[key];
            var marker = L.marker([station['latitude'], station['longitude']]);
            marker.addTo(map);
            marker.bindTooltip(station['name']);
            marker.on('click', onMarkerClick);
        }

    }
});
