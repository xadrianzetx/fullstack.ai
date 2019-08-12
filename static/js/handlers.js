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
        this.startingPoint = data['latlng'];

    }

    setEndPoint(data) {
        this.predicted = true;
        console.log(this.startingPoint);
        console.log(data['latlng']);
        // ajax post wiht this.startingPoint and data['latlng']
        // to flask /get_prediction with POST
        // return predicted

        return 'beep boop'
    }

    reset() {
        // reset state and get ready for next pred
        this.startPointSet = false;
        this.predicted = false;
        console.log('reset');
    }
}
