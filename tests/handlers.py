from __future__ import absolute_import
import mock
import unittest

from handlers import RequestHandler
from storage import InMemoryStorage

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

    def test_validate_good_path(self):
        mock_handler = self._create_mock_handler('/set?somekey=somevalue')
        mock_handler.parse()

    @mock.patch.object(RequestHandler, 'handle_error')
    def test_validate_bad_path(self, mock_call):
        mock_handler = self._create_mock_handler('/')
        with self.assertRaises(ValueError):
            mock_handler.parse()

        mock_handler = self._create_mock_handler('/bad_path')
        with self.assertRaises(ValueError):
            mock_handler.parse()

        # cannot set multiple values for same queryparam
        mock_handler = self._create_mock_handler('/set?fruit=pear&fruit=plum')
        with self.assertRaises(ValueError):
            mock_handler.parse()

        # missing queryparams
        mock_handler = self._create_mock_handler('/set')
        with self.assertRaises(ValueError):
            mock_handler.parse()

        # missing queryparams
        mock_handler = self._create_mock_handler('/get')
        with self.assertRaises(ValueError):
            mock_handler.parse()

    @mock.patch.object(RequestHandler, 'handle_ok')
    def test_do_GET(self, mock_call):

        mock_handler = self._create_mock_handler('/set?fruit=apple')
        mock_handler.do_GET()
        mock_call.assert_called_with('OK\n')

        mock_handler = self._create_mock_handler('/get?key=fruit')
        mock_handler.do_GET()
        mock_call.assert_called_with('apple\n')


    def tearDown(cls):

        # have to reset in order to avoid stepping on other tests
        InMemoryStorage.CONTAINER = {}

    def _create_mock_handler(self, path):

        class MockRequestHandler(RequestHandler):
            def __init__(self, path):
                self.path = path

        return MockRequestHandler(path)
