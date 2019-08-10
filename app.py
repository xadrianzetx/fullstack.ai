import os
import json
from flask import Flask, Response, render_template, request
from backend.preprocessing import TripTimePreprocessor
from backend.models import TripTimeEstimator


APP = Flask(__name__)


def get_trip_time(start_id, end_id):
    """
    Trip time prediction using k boosted trees

    :param start_id:    str
                        start station id
    :param end_id:      str
                        end station id

    :return:            pred float
                        predicted trip time (in minutes)
                        valid bool
                        true if valid station ids were passed
    """
    prep = TripTimePreprocessor()
    model = TripTimeEstimator(n_folds=10)
    valid = True

    try:
        # build feature array based on station id
        prep.set(start_id, mode='start')
        prep.set(end_id, mode='end')

        # run preprocessing and inference
        data = prep.transform()
        pred = model.predict(data)

    except KeyError:
        # one or more id invalid
        pred = 0.
        valid = False

    return pred, valid


@APP.route('/')
def index():
    """
    User interface
    """
    return render_template('index.html')


@APP.route('/api', methods=['GET'])
def api():
    """
    API interface - trip time prediction
    example call: /api?start=42&end=63

    GET:    json
            predicted travel time form
            start station to end station
            and metadata
    """
    # get station ids and run inference
    start_id = request.args.get('start', type=str)
    end_id = request.args.get('end', type=str)
    pred, valid = get_trip_time(start_id, end_id)

    if valid:
        path = 'backend/assets/station_data/'
        file = 'station_names.json'

        with open(os.path.join(path, file), 'r') as f:
            # load json with metadata and add to response
            data = json.load(f)
            start = data[start_id]
            end = data[end_id]
            payload = {'start': start, 'destination': end, 'time_predicted': pred}

        payload = json.dumps(payload, indent=4)
        code = 200

    else:
        # could not find station in lookup
        payload = {'error: Invalid station id passed to API'}
        code = 404

    return Response(payload, status=code, mimetype='application/json')


@APP.route('/api/stations', methods=['GET'])
def api_stations():
    """
    API interface - station info

    GET:    json
            valid station ids with names
    """
    path = 'backend/assets/station_data/'
    file = 'station_names.json'

    with open(os.path.join(path, file), 'r') as f:
        data = json.load(f)
        payload = {}

        for key in data.keys():
            # load json with station ids and names
            payload[key] = data[key]['name']

    return Response(json.dumps(payload, indent=4), status=200, mimetype='application/json')


if __name__ == '__main__':
    APP.run(debug=True)
