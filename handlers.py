from BaseHTTPServer import BaseHTTPRequestHandler
from storage import InMemoryStorage
from urlparse import parse_qs


class RequestHandler(BaseHTTPRequestHandler):
    """
    Main request handler
    """

    STORAGE = InMemoryStorage()
    SUPPORTED_PATHS = ('get', 'set')

    def do_GET(self):
        """
        Handles GET requests. All other requests return 501.

        Note that query params are stored as a list, but our validation
        ensures only one value is stored for a given key, we therefore store
        and retrieve the first element provided.

        :return: None
        :rtype: None
        """
        try:
            path, params = self.parse()
        except ValueError:
            return

        if(path == 'set'):
            self.STORAGE.store_multiple({k: v[0] for k,v in params.iteritems()})
            self.handle_ok("OK\n")
        elif(path == 'get'):
            self.handle_ok("%s\n" % self.STORAGE.retrieve(params['key'][0]))
        else:
            self.handle_error(400, "%s is an invalid path, please try again\n" % path)

    def parse(self):
        """
        Parse provided path and query params for validation and key
        setting/retrieval.

        :return: the parsed path and params (e.g. ('set', {'fruit': ['apple']})
        :rtype: (str, dict)
        :raises: ValueError
        """
        if '?' not in self.path:
            self.handle_error(
                400, "%s is an invalid path, please try again\n" % self.path)
            raise ValueError

        delim_idx = self.path.index('?')
        parsed_path  = self.path[1:delim_idx]
        params = parse_qs(self.path[delim_idx+1:])
        self.validate(parsed_path, params)
        return parsed_path, params

    def validate(self, parsed_path, params):
        """
        Validate the given path and params.

        :param parsed_path: the path (e.g. "set")
        :type parsed_path: str
        :param params: the query params (e.g. {"fruit": ["apple"]})
        :type params: dict
        :return: None
        :rtype: None
        :raises: ValueError
        """
        self.validate_path(parsed_path)
        self.validate_params(parsed_path, params)

    def validate_path(self, parsed_path):
        """
        Validate the given path. Currently supports `get` and `set`.

        :param parsed_path: the parsed path
        :type parsed_path: str
        :return: None
        :rtype: None
        :raises: ValueError
        """
        if parsed_path not in self.SUPPORTED_PATHS:
            self.handle_error(
                400, "%s is an invalid path, please try again\n" % self.path)
            raise ValueError

    def validate_params(self, parsed_path, params):
        """
        Validate the given params. Requirements: only one value per queryparam
        and only one key can be retrieved at a time.

        :param parsed_path: the parsed path
        :type parsed_path: str
        :param params: the queryparams
        :type params: dict
        :return: None
        :rtype: None
        :raises: ValueError
        """

        for param, val in params.iteritems():
            if len(val) > 1:
                self.handle_error(
                    400, "Error: multiple values provided for key %s" % param)
                raise ValueError

        if parsed_path == 'get':
            if(len(params) != 1 or 'key' not in params):
                self.handle_error(
                    400, "Retrieval queries only support the 'key' query "
                         "parameter\n"
                )
                raise ValueError


    def handle_ok(self, response_body):
        """
        Handles the sending of OK responses.

        :param response_body: response body to be sent
        :type response_body: str
        :return: None
        :rtype: None
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_body)

    def handle_error(self, status_code, response_body):
        """
        Handles the sending of bad responses.

        :param status_code: status code to be sent
        :type status_code: int
        :param response_body: response body to be sent
        :type response_body: str
        :return: None
        :rtype: None
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_body)
