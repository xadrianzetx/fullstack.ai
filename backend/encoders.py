import numpy as np
import pandas as pd


class RobustOneHotEncoder:

    def __init__(self):
        self.pos = 0
        self.columns = None
        self.categories = None
        # TODO support for multiple feats
        # TODO tests

    def _get_categories(self, df, col):
        """

        :param df:
        :param col:
        :return:
        """
        self.columns = col
        self.pos = np.where(df.columns == col)[0][0]
        cats = sorted(df.iloc[:, self.pos].value_counts(dropna=True).index)

        return cats

    def fit(self, df, col):
        """

        :param df:
        :param col:
        :return:
        """
        assert col in df.columns
        self.categories = self._get_categories(df, col)

    def fit_transform(self, df, col):
        """

        :param df:
        :param col:
        :return:
        """
        assert col in df.columns
        self.categories = self._get_categories(df, col)
        t = pd.api.types.CategoricalDtype(categories=self.categories)
        labels = df.iloc[:, [self.pos]].astype(t)
        encoded = pd.merge([df, pd.get_dummies(labels)], axis=1)
        encoded = encoded.drop([self.columns], axis=1)

        return encoded

    def transform(self, df):
        """

        :param df:
        :return:
        """
        t = pd.api.types.CategoricalDtype(categories=self.categories)
        labels = df.iloc[:, [self.pos]].astype(t)
        encoded = pd.merge([df, pd.get_dummies(labels)], axis=1)
        encoded = encoded.drop([self.columns], axis=1)

        return encoded

    def save_encoder(self):
        pass
