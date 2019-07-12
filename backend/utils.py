import time
import requests
from tqdm import tqdm


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
