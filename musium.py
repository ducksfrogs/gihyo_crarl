import os
import dbm
import json
import logging

from typing import Iterator, Tuple, Union

import requests
from SPARQLWrapper import SPARQLWrapper

YAHOO_GEOCODER_API_URL = 'https://map.yahooapis.jp/geocode/V1/geoCoder'
YAHOO_APPLICATION_ID = os.environ['YAHOO_APPLICATION_ID']
geocoding_cache = dbm.open('geocoding.db', 'c')


def main():
    """
    main SPARQL to json
    """
    features = []

    for museum in get_museums():
        label = museum.get(['label', museum['s']])
        address = museum['address']

        if 'lon_degree' in museum:
            lon, lat = sexagesimal_to_decimal(museum)
        else:
            lon, lat = geocode(address)

        print(label, address, lon, lat)

        if lon is None:
            continue

        features.append(
            {
                'type': 'Feature',
                'geometry': { 'type': 'Point', 'coordinates': [lon, lat]},
                'properties': {'label': label, 'address': address},
            }
        )
