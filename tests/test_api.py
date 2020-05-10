import json
import unittest
from app import APP


class TestApplicationAPI(unittest.TestCase):
    
    def test_station_list_get(self):
        response = APP.test_client().get(
            '/api/stations'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_station_list_post(self):
        response = APP.test_client().post(
            '/api/stations'
        )
        self.assertEqual(response.status_code, 405)
    
    def test_api_inference_correct_codes(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 73, 'end': 39}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_api_inference_incorrect_start(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 1e4, 'end': 39}
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_incorrect_end(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 73, 'end': 1e4}
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_out_of_town_start(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 9, 'end': 73}
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_out_of_town_end(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 73, 'end': 36}
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_json_passed(self):
        response = APP.test_client().get(
            '/api',
            data=json.dumps({'start': 73, 'end': 39})
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_empty_param(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 73, 'end': None}
        )
        self.assertEqual(response.status_code, 404)

    def test_api_inference_missing_param(self):
        response = APP.test_client().get(
            '/api',
            query_string={'start': 73}
        )
        self.assertEqual(response.status_code, 404)
    
    def test_api_inference_post(self):
        response = APP.test_client().post(
            '/api',
            query_string={'start': 73, 'end': 39}
        )
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
