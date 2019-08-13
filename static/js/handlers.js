class MapEventHandler {
    constructor() {
        this.startPointSet = false;
        this.predicted = false;
    }

    get isStartPointSet() {
        return this.startPointSet;
    }

    get isPredicted() {
        return this.predicted;
    }

    setStartPoint(data) {
        // set starting location
        this.startPointSet = true;
        this.startStationId = data.target.options.id;
    }

    setEndPoint(data) {
        this.predicted = true;
        var endStationId = data.target.options.id;

        // POST to server and return call to await response
        var call = $.ajax({
            type: 'POST',
            url: '/get_prediction',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({start: this.startStationId, end: endStationId}),
        });

        return call;
    }

    reset() {
        // reset state and get ready for next pred
        this.startPointSet = false;
        this.predicted = false;
    }
}
