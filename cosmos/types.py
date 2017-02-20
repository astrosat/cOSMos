from collections import namedtuple

from cosmos.constants import (JSON_QUERY_TEMPLATE,
                              ROAD_QUERY, CITY_QUERY, BUILDING_QUERY)


def linestrings(elements):
    return (
        [(float(coordinate['lon']), float(coordinate['lat']))
         for coordinate in element['geometry']]
        for element in elements)


def polygons(elements):
    return (
        [[(float(coordinate['lon']), float(coordinate['lat']))
          for coordinate in element['geometry']]]
        for element in elements)


def points(elements):
    return ((float(element['lon']), float(element['lat']))
            for element in elements)


def road_query(bbox):
    return JSON_QUERY_TEMPLATE.format(*(bbox + ROAD_QUERY))


def building_query(bbox):
    return JSON_QUERY_TEMPLATE.format(*(bbox + BUILDING_QUERY))


def city_query(bbox):
    return JSON_QUERY_TEMPLATE.format(*(bbox + CITY_QUERY))

BoundingBox = namedtuple('BoundingBox', ('left', 'top', 'right', 'bottom'))

DataType = {
    'roads': {
        'geometry': 'LineString',
        'features': linestrings,
        'query': road_query,
        'element': 'way'
    },
    'cities': {
        'geometry': 'Point',
        'features': points,
        'query': city_query,
        'element': 'node'
    },
    'buildings': {
        'geometry': 'Polygon',
        'features': polygons,
        'query': building_query,
        'element': 'way'
    }
}
