import unittest
from backend import utils


class TestHaversine(unittest.TestCase):

    def test_distance_float(self):
        """

        Test behaviour with correct input
        """
        p1 = (52.398382, 16.924408)
        p2 = (52.202013, 21.014115)
        result = utils.haversine_distance(p1, p2)
        self.assertEqual(round(result, 4), 278.9993)

    def test_distance_int(self):
        """

        Test behaviour with integers
        """
        p1 = (52, 16)
        p2 = (52, 21)

        with self.assertRaises(AssertionError):
            utils.haversine_distance(p1, p2)

    def test_distance_str(self):
        """

        Test behaviour with strings
        """
        p1 = ('52.398382', '16.924408')
        p2 = ('52.202013', '21.014115')

        with self.assertRaises(AssertionError):
            utils.haversine_distance(p1, p2)

    def test_p1_elements_num(self):
        """

        Test incorrect number of coordinates for location 1
        """
        p1 = (52.398382, 16.924408, 16.924408)
        p2 = (52.202013, 21.014115)

        with self.assertRaises(AssertionError):
            utils.haversine_distance(p1, p2)

    def test_p2_elements_num(self):
        """

        Test incorrect number of coordinates for location 2
        """
        p1 = (52.398382, 16.924408)
        p2 = (52.202013, 21.014115, 21.014115)

        with self.assertRaises(AssertionError):
            utils.haversine_distance(p1, p2)
