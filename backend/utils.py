import time
import requests
import numpy as np
import lightgbm as lgb
from tqdm import tqdm
from math import sin, cos, sqrt, atan2, radians
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


def map_altitudes(data, api_key):
    """
    Maps altitude data to latitude longitude pairs
    using https://developers.google.com/maps/documentation/elevation/intro

    :param data:    dict
                    lat lon data
    :param api_key: string
                    api key

    :return:        dict
                    data with mapped altitudes
    """
    url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key={}'
    out = {}

    for key in tqdm(data.keys()):
        # list of coordinates [lat, lon]
        coords = data[key]
        r = requests.get(url=url.format(coords[0], coords[1], api_key))
        payload = r.json()
        out[key] = {'data': coords, 'altitude': payload['results'][0]['elevation']}

        # API key restrictions
        time.sleep(2)

    return out


def haversine_distance(a, b):
    """
    https://en.wikipedia.org/wiki/Haversine_formula

    :param a:   tuple
                coord a (lat, long)
    :param b:   tuple
                coord b (lat, long)

    :return:    float
                distance between a and b in km
    """
    assert len(a) == 2 and len(b) == 2
    assert isinstance(a[0], float) and isinstance(a[1], float)
    assert isinstance(b[0], float) and isinstance(b[1], float)

    r = 6373.0

    a = [radians(x) for x in a]
    b = [radians(x) for x in b]

    diff = [x - y for x, y in zip(a, b)]
    a = sin(diff[0] / 2) ** 2 + cos(a[0]) * cos(b[0]) * sin(diff[1] / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    dist = r * c

    return dist


def lgbm_regression_cv(x, y, params, cv=10):
    """
    Objective function for skopt Bayesian optimization

    :param x:       numpy array NxM
                    features
    :param y:       numpy array N
                    response
    :param params:  dict
                    lgbm model parameters
    :param cv:      int
                    number of folds

    :return:        float
                    evaluation metric (MSE)
    """
    cv_pred = np.zeros(len(y))
    kf = KFold(n_splits=cv, shuffle=True, random_state=42)

    for train_idx, valid_idx in kf.split(x, y):
        x_train, y_train = x[train_idx], y[train_idx]
        x_valid, y_valid = x[valid_idx], y[valid_idx]

        # convert to lgb.Dataset
        y_train = y_train.ravel()
        y_valid = y_valid.ravel()
        lgb_train = lgb.Dataset(x_train, y_train)
        lgb_valid = lgb.Dataset(x_valid, y_valid)

        clf = lgb.train(params,
                        lgb_train,
                        num_boost_round=1000,
                        valid_sets=lgb_valid,
                        early_stopping_rounds=5)

        cv_pred[valid_idx] = clf.predict(x_valid, num_iteration=clf.best_iteration)

    # exponential to get back from log response
    cv_pred = [np.expm1(i) for i in cv_pred]
    y = [np.expm1(i) for i in y]

    return mean_squared_error(y, cv_pred)
