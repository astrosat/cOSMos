import json

from unittest import TestCase
from unittest.mock import patch

from geojson import FeatureCollection
from geopy import Location

from cosmos.utils import compute_geojson, process_osm_output, coords_for
from cosmos.types import DataType, BoundingBox


class TestUtils(TestCase):

    def setUp(self):
        with open('tests/data/roads.json') as f:
            self.roads_data = json.load(f)
        with open('tests/data/buildings.json') as f:
            self.buildings_data = json.load(f)
        with open('tests/data/cities.json') as f:
            self.cities_data = json.load(f)

    def test_should_raise_error_when_incorrect_geometry_type(self):
        data_type = DataType['roads']
        data_type['geometry'] = 'unknown'

        with self.assertRaises(AttributeError):
            compute_geojson(data_type, ())

    def test_should_retrieve_geojson_from_osm_output(self):
        data_type = DataType['roads']
        data_type['geometry'] = 'LineString'

        output = process_osm_output(self.roads_data, data_type, 'geojson')

        self.assertIsInstance(output, FeatureCollection)

    def test_should_retrieve_two_lists_from_osm_output(self):
        data_type = DataType['roads']

        output1, output2 = process_osm_output(
            self.roads_data, data_type, format='')

        self.assertIsInstance(list(output1), list)
        self.assertIsInstance(list(output2), list)

    def test_should_compute_geojson_with_roads_linestrings(self):
        data_type = DataType['roads']

        output = process_osm_output(self.roads_data, data_type, 'geojson')

        self.assertIsInstance(output, FeatureCollection)
        self.assertEqual('LineString', output['features'][
                         0]['geometry']['type'])

    def test_should_compute_geojson_with_buildings_polygons(self):
        data_type = DataType['buildings']

        output = process_osm_output(self.buildings_data, data_type, 'geojson')

        self.assertIsInstance(output, FeatureCollection)
        self.assertEqual('Polygon', output['features'][
                         0]['geometry']['type'])

    def test_should_compute_geojson_with_cities_points(self):
        data_type = DataType['cities']

        output = process_osm_output(self.cities_data, data_type, 'geojson')

        self.assertIsInstance(output, FeatureCollection)
        self.assertEqual('Point', output['features'][
                         0]['geometry']['type'])

    @patch('cosmos.utils.Nominatim.geocode')
    def test_should_retrieve_bbox_from_location_name_for_point(
            self, mocked_geocode):
        bbox = (0.0, 1.0, 2.0, 3.0)
        location = Location(raw={
            'boundingbox': bbox,
            'geojson':
            {
                'coordinates': [-79.6371123, 39.2138905],
                'type': 'Point'
            }
        })
        mocked_geocode.return_value = location

        output = coords_for('test')

        self.assertEqual(output, (bbox[0], bbox[2], bbox[1], bbox[3]))

    @patch('cosmos.utils.Nominatim.geocode')
    def test_should_retrieve_bbox_from_location_name_for_polygon(
            self, mocked_geocode):
        bbox = (0.0, 1.0, 2.0, 3.0)
        location = Location(raw={
            'boundingbox': bbox,
            'geojson':
            {
                'coordinates': [
                    [
                        [
                            -3.0938758,
                            55.9348096
                        ],
                        [
                            -3.0938096,
                            55.9346675
                        ],
                        [
                            -3.0934263,
                            55.9347236
                        ],
                        [
                            -3.0934925,
                            55.9348656
                        ],
                        [
                            -3.0938758,
                            55.9348096
                        ]
                    ]
                ],
                'type': 'Polygon'
            }
        })
        mocked_geocode.return_value = location

        output = coords_for('test')

        self.assertIsInstance(output, BoundingBox)

    @patch('cosmos.utils.Nominatim.geocode')
    def test_should_retrieve_bbox_from_location_name_for_multipolygon(
            self, mocked_geocode):
        bbox = (0.0, 1.0, 2.0, 3.0)
        location = Location(raw={
            'boundingbox': bbox,
            'geojson':
            {
                'coordinates': [
                    [[
                        [
                            -3.0938758,
                            55.9348096
                        ],
                        [
                            -3.0938096,
                            55.9346675
                        ],
                        [
                            -3.0934263,
                            55.9347236
                        ],
                        [
                            -3.0934925,
                            55.9348656
                        ],
                        [
                            -3.0938758,
                            55.9348096
                        ]
                    ]],
                    [[
                        [
                            9.6240234375,
                            52.429222277955134
                        ],
                        [
                            12.3486328125,
                            52.429222277955134
                        ],
                        [
                            12.3486328125,
                            53.85252660044951
                        ],
                        [
                            9.6240234375,
                            53.85252660044951
                        ],
                        [
                            9.6240234375,
                            52.429222277955134
                        ]
                    ]]
                ],
                'type': 'MultiPolygon'
            }
        })
        mocked_geocode.return_value = location

        output = list(coords_for('test'))

        self.assertIsInstance(output[0], BoundingBox)
        self.assertIsInstance(output[1], BoundingBox)
        self.assertEqual(len(output), 2)

    @patch('cosmos.utils.Nominatim.geocode', return_value={})
    def test_should_raise_attr_error_when_bbox_not_found(self, mocked_geocode):
        with self.assertRaises(AttributeError):
            coords_for('test')
