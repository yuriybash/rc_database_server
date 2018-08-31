from __future__ import absolute_import
import mock
import unittest

from handlers import RequestHandler

class RequestHandlerTest(unittest.TestCase):


    def test_parse_good_path_good_params(self):

        mock_handler = self._create_mock_handler('/set?somekey=somevalue')
        parsed_path, params = mock_handler.parse()
        self.assertEqual('set', parsed_path)
        self.assertEqual({'somekey': ['somevalue']}, params)

    @mock.patch.object(RequestHandler, 'handle_error')
    def test_parse_good_path_bad_params(self, mock_call):

        mock_handler = self._create_mock_handler('/get?badparam=badval')
        with self.assertRaises(ValueError):
            mock_handler.parse()

    @mock.patch.object(RequestHandler, 'handle_error')
    def test_parse_bad_path(self, mock_call):

        mock_handler = self._create_mock_handler('/invalid')
        with self.assertRaises(ValueError):
            mock_handler.parse()


    def _create_mock_handler(self, path):

        class MockRequestHandler(RequestHandler):
            def __init__(self, path):
                self.path = path

        return MockRequestHandler(path)
