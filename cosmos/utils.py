import geojson
from geojson import Feature, FeatureCollection
from geopy.geocoders import Nominatim
from shapely.geometry import shape

from cosmos.types import BoundingBox


def compute_geojson(data_type, elements):
    geojson_features = ()
    features = data_type['features'](elements)
    tags = (element.get('tags') for element in elements)

    try:
        geometry = getattr(geojson, data_type['geometry'])
        geojson_features = (Feature(geometry=geometry(feature), properties=tag)
                            for feature, tag in zip(features, tags))
    except AttributeError:
        raise AttributeError('Invalid geometry type in data_type.')

    return FeatureCollection(list(geojson_features))


def extract_elements_from_osm(data, element_type):
    return (element for element in data[
        'elements'] if element['type'] == element_type)


def process_osm_output(data, data_type, format):
    features = ()
    tags = ()
    elements = []

    if isinstance(data, list):
        for d in data:
            elements.extend(
                list(extract_elements_from_osm(d, data_type['element'])))
    else:
        elements = list(extract_elements_from_osm(data, data_type['element']))

    if format == 'geojson':
        return compute_geojson(data_type, elements)
    else:
        features = data_type['features'](elements)
        tags = (element.get('tags') for element in elements)

    return features, tags


def coords_for(name):
    geocoder = Nominatim()
    location = geocoder.geocode(name, geometry='geojson')

    try:
        geometry = shape(location.raw['geojson'])

        # Coordinates have to be flipped in order to work in overpass
        if geometry.geom_type == 'Polygon':
            top, left, bottom, right = geometry.bounds
            return BoundingBox(left, top, right, bottom)

        elif geometry.geom_type == 'MultiPolygon':
            bboxs = (BoundingBox(*(g.bounds[0:2][::-1] + g.bounds[2:][::-1]))
                     for g in geometry)
            return bboxs
        elif geometry.geom_type == 'Point':
            left, right, top, bottom = (float(coordinate)
                                        for coordinate in
                                        location.raw['boundingbox'])
            return BoundingBox(left, top, right, bottom)

    except (KeyError, AttributeError):
        raise AttributeError(
            'No bounding box available for this location name.')
