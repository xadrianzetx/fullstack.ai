import json
from flask import Flask, Response, render_template, request
from backend.preprocessing import TripTimePreprocessor
from backend.models import TripTimeEstimator


app = Flask(__name__)


def get_trip_time(start_id, end_id):
    prep = TripTimePreprocessor()
    model = TripTimeEstimator(n_folds=10)
    valid = True

    try:
        prep.set(start_id, mode='start')
        prep.set(end_id, mode='end')
        data = prep.transform()
        pred = model.predict(data)

    except KeyError:
        pred = None
        valid = False

    return pred, valid


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api():
    # example call /api?start=42&end=63
    start_id = request.args.get('start', type=str)
    end_id = request.args.get('end', type=str)
    pred, valid = get_trip_time(start_id, end_id)

    if valid:
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

        payload = json.dumps(payload)
        code = 200

    else:
        # could not find station in lookup
        payload = {'error: Invalid station id passed to API'}
        code = 404

    return Response(payload, status=code, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
