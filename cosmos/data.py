import requests

from cosmos.constants import OVERPASS_API_URL, RESPONSE_TIMEOUT
from cosmos.utils import (process_osm_output, coords_for,
                          extract_elements_from_osm)
from cosmos.types import DataType, BoundingBox


class Data(object):
    '''
    Class to retrieve different objects from Overpass API
    '''

    def __init__(self, location=None):
        self.location = location

    def query_overpass(self, query):
        response = requests.post(
            OVERPASS_API_URL,
            query,
            RESPONSE_TIMEOUT
        )
        if response.ok:
            return response.json()

        return None

    def get(self, dtype='roads', location=None, format=None, bbox=None):
        data = []

        try:
            data_type = DataType[dtype]
        except KeyError:
            raise KeyError('Invalid data type.')

        if not bbox:
            if not location:
                location = self.location
            bbox = coords_for(location)

            if not isinstance(bbox, BoundingBox):
                for bb in bbox:
                    query = data_type['query'](bb)
                    data.append(self.query_overpass(query))

                return process_osm_output(data, data_type, format)

        query = data_type['query'](bbox)
        data = self.query_overpass(query)

        return process_osm_output(data, data_type, format)
