import types
from requests import Response
from geopy import Location

from unittest import TestCase
from unittest.mock import patch

from cosmos import Data


class TestData(TestCase):

    @patch('cosmos.utils.Nominatim.geocode', return_value={})
    @patch('cosmos.data.process_osm_output')
    def test_should_get_data_when_location_defined_on_instantiation(
            self, mocked_process_osm_output, mocked_geocode):
        test_data = ([1, 2], ['a', 'b'])
        mocked_process_osm_output.return_value = test_data
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

        data = Data('location')

        output1, output2 = data.get('roads')

        self.assertEqual(test_data, (list(output1), list(output2)))

    @patch('cosmos.utils.Nominatim.geocode')
    @patch('cosmos.data.process_osm_output')
    def test_should_get_data_when_location_defined_on_function_call(
            self, mocked_process_osm_output,
            mocked_geocode):
        test_data = ([1, 2], ['a', 'b'])
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
        mocked_process_osm_output.return_value = test_data
        data = Data()

        output = data.get('roads', 'location')

        self.assertEqual(test_data, output)

    @patch('cosmos.utils.Nominatim.geocode')
    def test_should_get_data_when_location_has_multiple_polygons(
            self,
            mocked_geocode):
        data = Data()

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

        output1, output2 = data.get('roads', 'location')

        self.assertIsInstance(output1, types.GeneratorType)
        self.assertIsInstance(output2, types.GeneratorType)

    @patch('cosmos.data.process_osm_output')
    def test_should_get_roads_data_when_bbox_defined_by_user(
            self, mocked_process_osm_output):
        test_data = ([1, 2], ['a', 'b'])
        mocked_process_osm_output.return_value = test_data
        data = Data()

        output = data.get('roads', bbox=(0, 1, 2, 3))

        self.assertEqual(test_data, output)

    @patch('cosmos.data.process_osm_output')
    def test_should_get_buildings_data_when_bbox_defined_by_user(
            self, mocked_process_osm_output):
        test_data = ([1, 2], ['a', 'b'])
        mocked_process_osm_output.return_value = test_data
        data = Data()

        output = data.get('buildings', bbox=(0, 1, 2, 3))

        self.assertEqual(test_data, output)

    @patch('cosmos.data.process_osm_output')
    def test_should_get_cities_data_when_bbox_defined_by_user(
            self, mocked_process_osm_output):
        test_data = ([1, 2], ['a', 'b'])
        mocked_process_osm_output.return_value = test_data
        data = Data()

        output = data.get('cities', bbox=(0, 1, 2, 3))

        self.assertEqual(test_data, output)

    def test_should_raise_error(self):
        data = Data('location')

        with self.assertRaises(KeyError):
            data.get('unknown')

    @patch('requests.post')
    def test_should_return_none_from_overpass(self, mocked_post):
        data = Data()
        test_response = Response()
        test_response.status_code = 400
        mocked_post.return_value = test_response

        output = data.query_overpass('query')

        self.assertEquals(None, output)

    @patch('requests.post')
    @patch('requests.Response.json')
    def test_should_return_json_from_overpass(self, mocked_json, mocked_post):
        mocked_json.return_value = '{}'
        data = Data()
        test_response = Response()
        test_response.status_code = 200
        mocked_post.return_value = test_response

        output = data.query_overpass('query')

        self.assertEquals('{}', output)
