import os
import pkg_resources
import lightgbm as lgb


class TripTimeEstimator:

    def __init__(self, n_folds):
        self._n_folds = n_folds
        self._models = self._load_models()

    def _load_models(self):
        models = []
        path = '/assets/'
        abs_path = pkg_resources.resource_filename('backend', path)
        artifacts = os.listdir(abs_path)

        if len(artifacts) != self._n_folds:
            raise ValueError('Number of model artifacts does not match n_folds')

        for artifact in artifacts:
            arti_path = os.path.join(abs_path, artifact)
            clf = lgb.Booster(model_file=arti_path)
            models.append(clf)

        return models

    def predict(self, data):
        pass
