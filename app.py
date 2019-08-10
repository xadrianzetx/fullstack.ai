import sys
import json
from flask import Flask, Response, render_template, request, abort
from backend.preprocessing import TripTimePreprocessor
from backend.models import TripTimeEstimator


app = Flask(__name__)


def get_trip_time(start_id, end_id):
    prep = TripTimePreprocessor()
    model = TripTimeEstimator(n_folds=10)

    try:
        prep.set(start_id, mode='start')
        prep.set(end_id, mode='end')

    except KeyError:
        raise

    data = prep.transform()
    pred = model.predict(data)

    return pred


@app.errorhandler(404)
def not_found(error):
    payload = {'error: Invalid station id passed to API'}
    return Response(payload, status=404, mimetype='application/json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api():
    # example call /api?start=42&end=63
    start_id = request.args.get('start', type=str)
    end_id = request.args.get('end', type=str)

    try:
        pred = get_trip_time(start_id, end_id)

    except KeyError:
        abort(404)

    payload = {
        'start':
            {
                'station_name': 'foo',
                'coordinates': [0, 0]
            },
        'end':
            {
                'station_name': 'bar',
                'coordinates': [0, 0]
            },
        'predicted_trip_time': pred
    }

    return Response(json.dumps(payload), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
