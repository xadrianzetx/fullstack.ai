import pickle
import numpy as np
import pandas as pd


class RobustOneHotEncoder:

    def __init__(self, categorical: list):
        self.columns = categorical
        self.metadata = {}
        self._fitted = False

    @staticmethod
    def _get_categories(df, col):
        """
        Finds position of column and unique categories

        :param df:  pandas.DataFrame
                    Original data frame
        :param col: list
                    Names of columns to encode

        :return:    cats: list
                    list of unique categories
                    pos: int
                    column position
        """
        pos = np.where(df.columns == col)[0][0]
        cats = sorted(df.iloc[:, pos].value_counts(dropna=True).index)

        return cats, pos

    def fit(self, df):
        """
        Fits one hot encoder to selected columns
        of data frame

        :param df:  pandas.DataFrame
                    Raw data frame

        :return:    void
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError('Expected instance of pandas DataFrame')

        if not all(col in df.columns for col in self.columns):
            raise ValueError('Could not find all columns to encode in DataFrame')

        for col in self.columns:
            # find position and categories of each column
            categories, position = self._get_categories(df, col)
            self.metadata[col] = {'categories': categories, 'position': position}

        self._fitted = True

    def transform(self, df):
        """
        Transforms data frame based on fitted
        one hot encoder

        :param df:  pandas.DataFrame
                    Raw data frame

        :return:    pandas.DataFrame
                    Original data frame with columns encoded
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError('Expected instance of pandas DataFrame')

        if not all(col in df.columns for col in self.columns):
            raise ValueError('Could not find all columns to encode in DataFrame')

        if not self._fitted:
            raise ValueError('Need to fit or load encoder first')

        for col in self.columns:
            # get column metadata
            categories = self.metadata[col]['categories']
            position = self.metadata[col]['position']

            # Specify levels and encode
            dtype = pd.api.types.CategoricalDtype(categories=categories)
            labels = df.iloc[:, [position]].astype(dtype)
            df = pd.concat([df, pd.get_dummies(labels)], axis=1)

        # drop original columns
        encoded = df.drop(self.columns, axis=1)

        return encoded

    def fit_transform(self, df):
        """
        Calls .fit() and .transform() in order
        matching scikit-learn API

        :param df:  pandas.DataFrame
                    Raw data frame

        :return:    pandas.DataFrame
                    Original data frame with columns encoded
        """
        try:
            self.fit(df)
            encoded = self.transform(df)

        except ValueError:
            raise

        return encoded

    def save_encoder(self, path):
        """
        Save fitted encoder metadata

        :param path:    string
                        Path to file

        :return:        void
        """
        if self._fitted:
            with open(path, 'wb') as file:
                pickle.dump(self.metadata, file)

        else:
            raise ValueError('Need to fit encoder first')

    def load_encoder(self, path):
        """
        Loads encoder metadata

        :param path:    string
                        Path to file

        :return:        void
        """
        with open(path, 'rb') as file:
            self.metadata = pickle.load(file)
            self._fitted = True
