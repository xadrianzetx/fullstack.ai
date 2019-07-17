import time
import requests
from tqdm import tqdm
from math import sin, cos, sqrt, atan2, radians


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
    r = 6373.0

    a = [radians(x) for x in a]
    b = [radians(x) for x in b]

    diff = [x - y for x, y in zip(a, b)]
    a = sin(diff[0] / 2) ** 2 + cos(a[0]) * cos(b[0]) * sin(diff[1] / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    dist = r * c

    return dist
