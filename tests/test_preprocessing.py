import unittest
import numpy as np
from backend.preprocessing import TripTimePreprocessor


class TestTripTimePreprocessor(unittest.TestCase):

    def test_loading_assets(self):
        """
        Test if assets are loading correctly
        """
        prep = TripTimePreprocessor()
        self.assertIsInstance(prep._coords, dict)

    def test_set_valid_start(self):
        """
        Test setting valid start point
        """
        station_id = '42'
        data = np.array([37.79728, -122.398436, 2.519689321517944])
        prep = TripTimePreprocessor()
        prep.set(station_id, mode='start')
        compare = [x == y for x, y in zip(prep._data[:2], data)]
        self.assertTrue(all(compare))

    def test_set_valid_end(self):
        """
        Test setting valid end point
        """
        station_id = '42'
        data = np.array([37.79728, -122.398436, 2.519689321517944])
        prep = TripTimePreprocessor()
        prep.set(station_id, mode='end')
        compare = [x == y for x, y in zip(prep._data[3:5], data)]
        self.assertTrue(all(compare))

    def test_set_valid_start_end(self):
        """
        Test setting valid start and end points
        """
        start_station_id = '42'
        start_data = np.array([37.79728, -122.398436, 2.519689321517944])
        end_station_id = '63'
        end_data = np.array([37.786978000000005, -122.39810800000001, 7.070822715759277])

        prep = TripTimePreprocessor()
        prep.set(start_station_id, mode='start')
        prep.set(end_station_id, mode='end')

        data = np.concatenate((start_data, end_data), axis=0)
        compare = [x == y for x, y in zip(prep._data[:5], data)]
        self.assertTrue(all(compare))

    def test_invalid_station_id(self):
        """
        Test selecting invalid station
        """
        station_id = '0'
        prep = TripTimePreprocessor()

        with self.assertRaises(KeyError):
            prep.set(station_id, mode='start')

    def test_invalid_station_id_dtype(self):
        """
        Test passing wrong dtype in station selection
        """
        station_id = 'a'
        prep = TripTimePreprocessor()

        with self.assertRaises(KeyError):
            prep.set(station_id, mode='start')

    def test_invalid_mode(self):
        """
        Test selecting invalid preprocessing mode
        """
        station_id = '42'
        prep = TripTimePreprocessor()

        with self.assertRaises(ValueError):
            prep.set(station_id, 'stop')

    def test_invalid_mode_dtype(self):
        """
        Test passing wrong dtype in mode selection
        """
        station_id = '42'
        prep = TripTimePreprocessor()

        with self.assertRaises(ValueError):
            prep.set(station_id, 0)

    def test_valid_transform(self):
        """
        Test preprocessing output for valid data
        """
        start_station_id = '42'
        start_data = np.array([37.79728, -122.398436, 2.519689321517944])
        end_station_id = '63'
        end_data = np.array([37.786978000000005, -122.39810800000001, 7.070822715759277])
        alt = np.array([1.1462523737069703])

        prep = TripTimePreprocessor()
        prep.set(start_station_id, mode='start')
        prep.set(end_station_id, mode='end')

        data = np.concatenate((start_data, end_data, alt), axis=0)
        payload = prep.transform()
        compare = [x == y for x, y in zip(data, payload)]
        self.assertTrue(all(compare))

    def test_transform_point_not_set(self):
        """
        Test calling transform when either start
        or end point has not been set
        """
        station_id = '42'
        prep = TripTimePreprocessor()
        prep.set(station_id, mode='start')

        with self.assertRaises(ValueError):
            prep.transform()


if __name__ == '__main__':
    unittest.main()
