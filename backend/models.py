import os
import pkg_resources
import numpy as np
import lightgbm as lgb


class TripTimeEstimator:

    def __init__(self, n_folds):
        self._n_folds = n_folds
        self._models = self._load_models()

    def _load_models(self):
        models = []
        path = '/assets/models'

        # localize model artifacts for all folds
        abs_path = pkg_resources.resource_filename('backend', path)
        artifacts = os.listdir(abs_path)

        if len(artifacts) != self._n_folds:
            raise ValueError('Number of model artifacts does not match n_folds')

        for artifact in artifacts:
            # load model from artifact
            arti_path = os.path.join(abs_path, artifact)
            clf = lgb.Booster(model_file=arti_path)
            models.append(clf)

        return models

    def predict(self, data):
        """
        Estimates trip time by averaging out of fold
        predictions from k lightgbm boosters

        :param data:    np.ndarray (7, )
                        array with preprocessed features

        :return:        float
                        predicted trip time (in minutes)
        """
        if not isinstance(data, np.ndarray):
            passed = type(data)
            raise ValueError('Expected data to be numpy array, got {} instead'.format(passed))

        if data.shape != (7, ):
            raise ValueError('Expected data shape to be (7, ) got {}'.format(data.shape))

        if any(np.isnan(data)):
            raise ValueError('Got NaN in data')

        if data.dtype is not np.dtype('float64'):
            raise ValueError('Expected data type to be float64, got {} instead'.format(data.dtype))

        # init pred and get weighted prediction
        # from each fold
        pred = 0.
        data = data.reshape(1, -1)

        for clf in self._models:
            # each pred is log(duration)
            log_pred = clf.predict(data)[0]
            pred += np.expm1(log_pred) / self._n_folds

        return pred
