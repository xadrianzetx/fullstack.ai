import os
import json
import pkg_resources
import numpy as np
from backend.utils import haversine_distance


class TripTimePreprocessor:

    def __init__(self):
        self._data = np.zeros((7, ))
        self._coords = self._load_lookup()
        self._set = [False, False]

    @staticmethod
    def _load_lookup():
        path = '/assets/station_data'
        abs_path = pkg_resources.resource_filename('backend', path)
        artifact = os.path.join(abs_path, 'coordinates.json')

        if not os.path.isfile(artifact):
            raise FileNotFoundError('Could not find {}'.format(artifact))

        with open(artifact, 'r') as file:
            coords = json.load(file)

        return coords

    def set(self, station_id, mode):
        """
        Sets start or end point for travel time prediction

        Retrieves relevant data based on station id and puts
        it in designated spot in array to match model requirements

        :param station_id:  str
                            station id matching one of those
                            in SF Bike data
        :param mode:        str
                            'start' sets station as starting point
                            'end' sets station as end point

        :return:            void
        """
        valid_ids = [int(i) for i in self._coords.keys()]

        try:
            int(station_id)

        except (ValueError, TypeError):
            raise KeyError('Invalid station id type passed to preprocessor')

        if int(station_id) not in valid_ids:
            raise KeyError('Invalid station id value passed to preprocessor')

        if mode not in ['start', 'end']:
            raise ValueError('Invalid mode passed to preprocessor')

        # load values from lookup
        alt = self._coords[station_id]['altitude']
        coords = self._coords[station_id]['data']

        if mode == 'start':
            self._data[0] = coords[0]
            self._data[1] = coords[1]
            self._data[2] = alt
            self._set[0] = True

        else:
            self._data[3] = coords[0]
            self._data[4] = coords[1]
            self._data[5] = alt
            self._set[1] = True

    def transform(self):
        """
        Transforms start and end points into model features

        :return:    np.ndarray
                    preprocessed feature array
        """
        if all(self._set):
            # get lon, lat for start and end point
            # and calculate distance
            a = (self._data[0], self._data[1])
            b = (self._data[3], self._data[4])
            self._data[6] = haversine_distance(a, b)

        else:
            raise ValueError('Need to set both start and end points first')

        return self._data
