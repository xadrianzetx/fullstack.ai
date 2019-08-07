import unittest
import numpy as np
import pandas as pd
from backend.encoders import RobustOneHotEncoder


class TestRobustUnitTest(unittest.TestCase):

    def test_output_shape(self):
        """
        Test expected output shape
        """
        df = pd.DataFrame({'foo': [1, 2], 'bar': [1, 2], 'baz': [1, 2]})
        enc = RobustOneHotEncoder(['foo', 'bar'])
        encoded = enc.fit_transform(df)
        self.assertEqual(encoded.shape[1], 5)

    def test_input_type(self):
        """
        Test behaviour with wrong input type
        """
        df = np.zeros((10, 10))
        enc = RobustOneHotEncoder(['foo', 'bar'])

        with self.assertRaises(ValueError):
            enc.fit(df)

    def test_columns_type(self):
        """
        Test wrong type of column names
        """
        df = pd.DataFrame({'foo': [1, 2], 'bar': [1, 2], 'baz': [1, 2]})
        enc = RobustOneHotEncoder([1, 0])

        with self.assertRaises(ValueError):
            enc.transform(df)

    def test_input_missing(self):
        """
        Test columns missing in df
        """
        df = pd.DataFrame({'bar': [1, 2], 'baz': [1, 2]})
        enc = RobustOneHotEncoder(['foo', 'bar'])

        with self.assertRaises(ValueError):
            enc.fit(df)

    def test_encoder_not_fitted(self):
        """
        Test behaviour when encoder wasn't fitted
        """
        df = pd.DataFrame({'foo': [1, 2], 'bar': [1, 2], 'baz': [1, 2]})
        enc = RobustOneHotEncoder(['foo', 'bar'])

        with self.assertRaises(ValueError):
            enc.transform(df)


if __name__ == '__main__':
    unittest.main()