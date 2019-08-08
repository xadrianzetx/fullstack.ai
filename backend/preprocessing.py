import os
import json
import pkg_resources
import numpy as np
from backend.utils import haversine_distance


class TripTimePreprocessor:

    def __init__(self):
        self._data = np.zeros((7, ))
        self._coords = self._load_lookup()
        self._start_set = False
        self._end_set = False

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

    def set_start_point(self, station_id):
        """

        :param station_id:
        :return:
        """
        valid_ids = [int(i) for i in self._data.keys()]

        try:
            int(station_id)

        except (ValueError, TypeError):
            raise KeyError('Invalid station id type passed to preprocessor')

        if int(station_id) not in valid_ids:
            raise KeyError('Invalid station id value passed to preprocessor')

        # load values from lookup
        alt = self._coords[station_id]['altitude']
        coords = self._coords[station_id]['data']

        # set start values in correct order
        self._data[0] = coords[0]
        self._data[1] = coords[1]
        self._data[2] = alt
        self._start_set = True

    def set_end_point(self, station_id):
        """

        :param station_id:
        :return:
        """
        valid_ids = [int(i) for i in self._data.keys()]

        try:
            int(station_id)

        except (ValueError, TypeError):
            raise KeyError('Invalid station id type passed to preprocessor')

        if int(station_id) not in valid_ids:
            raise KeyError('Invalid station id value passed to preprocessor')

        # load values from lookup
        alt = self._coords[station_id]['altitude']
        coords = self._coords[station_id]['data']

        # set start values in correct order
        self._data[3] = coords[0]
        self._data[4] = coords[1]
        self._data[5] = alt
        self._end_set = True

    def transform(self):
        pass
