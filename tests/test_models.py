import os
import unittest
import numpy as np
from backend.models import TripTimeEstimator


class TestTripTimeEstimator(unittest.TestCase):

    def test_artifact_load(self):
        """
        Test loading artifacts
        """
        n_folds = len(os.listdir('backend/assets/models'))
        model = TripTimeEstimator(n_folds=n_folds)
        n_estimators = len(model._models)
        self.assertEqual(n_folds, n_estimators)

    def test_artifact_missing(self):
        """
        Test loading incorrect number of artifacts (missing)
        """
        n_folds = len(os.listdir('backend/assets/models')) + 1

        with self.assertRaises(ValueError):
            TripTimeEstimator(n_folds=n_folds)

    def test_artifacts_extra(self):
        """
        Test loading incorrect number of artifacts (extra)
        """
        n_folds = len(os.listdir('backend/assets/models')) - 1

        with self.assertRaises(ValueError):
            TripTimeEstimator(n_folds=n_folds)

    def test_input_correct(self):
        """
        Test output type with correct input
        """
        data = np.ones((7, ))
        model = TripTimeEstimator(n_folds=10)
        pred = model.predict(data)
        self.assertIsInstance(pred, float)

    def test_input_shape_zero(self):
        """
        Test malformed input (incorrect number of features)
        """
        data = np.ones((8, ))
        model = TripTimeEstimator(n_folds=10)

        with self.assertRaises(ValueError):
            model.predict(data)

    def test_input_shape_one(self):
        """
        Test malformed input (incorrect array shape)
        """
        data = np.ones((7, 1))
        model = TripTimeEstimator(n_folds=10)

        with self.assertRaises(ValueError):
            model.predict(data)

    def test_input_type(self):
        """
        Test passing list instead of np.ndarray
        """
        data = [1., 1., 1.]
        model = TripTimeEstimator(n_folds=10)

        with self.assertRaises(ValueError):
            model.predict(data)

    def test_input_dtype(self):
        """
        Test features with incorrect data type
        """
        data = np.array(['a', 'a', 'a'])
        model = TripTimeEstimator(n_folds=10)

        with self.assertRaises(ValueError):
            model.predict(data)

    def test_input_missing(self):
        """
        Test behaviour with NaN
        """
        data = np.ones((7, ))
        data[0] = np.nan
        model = TripTimeEstimator(n_folds=10)

        with self.assertRaises(ValueError):
            model.predict(data)


if __name__ == '__main__':
    unittest.main()
