from BaseHTTPServer import BaseHTTPRequestHandler
from storage import InMemoryStorage
from urlparse import parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    STORAGE = InMemoryStorage()

    def do_GET(self):
        try:
            path, params = self.parse()
        except ValueError:
            return

        if(path == 'set'):
            self.STORAGE.store_multiple(params)
            self.handle_ok("OK\n")
        elif(path == 'get'):
            self.handle_ok("%s\n" % self.STORAGE.retrieve(params['key'][0]))
        else:
            self.handle_error(400, "%s is an invalid path, please try again\n" % path)

    def parse(self):
        delim_idx = self.path.index('?')

        if not delim_idx:
            self.handle_error(
                400, "%s is an invalid path, please try again\n" % self.path)
            return

        parsed_path  = self.path[1:delim_idx]
        params = parse_qs(self.path[delim_idx+1:])
        self.validate(parsed_path, params)
        return parsed_path, params

    def validate(self, parsed_path, params):
        self.validate_path(parsed_path)
        self.validate_params(parsed_path, params)

    def validate_path(self, parsed_path):
        if parsed_path not in ('get', 'set'):
            self.handle_error(
                400, "%s is an invalid path, please try again\n" % self.path)
            raise ValueError

    def validate_params(self, parsed_path, params):

        for param, val in params.iteritems():
            if len(val) > 1:
                self.handle_error(
                    400, "Error: multiple values provided for key %s" % param)
                raise ValueError

        if parsed_path == 'get':
            if(len(params) != 1 or 'key' not in params):
                self.handle_error(
                    400, "Retrieval queries only support the 'key' queryparam")
                raise ValueError


    def handle_ok(self, response_body):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_body)

    def handle_error(self, status_code, response_body):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_body)
