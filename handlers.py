from BaseHTTPServer import BaseHTTPRequestHandler
from storage import InMemoryStorage
from urlparse import parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    STORAGE = InMemoryStorage()

    def do_GET(self):
        path, params = self.parse()

        if(path == 'set'):
            self.STORAGE.store_multiple(params)
            self.handle_ok("OK\n")
        elif(path == 'get'):
            self.handle_ok("%s\n" % self.STORAGE.retrieve(params['key'][0]))
        else:
            self.handle_error(400, "%s is an invalid path, please try again\n" % path)

    def parse(self):
        delim_idx = self.path.index('?')
        path  = self.path[1:delim_idx]
        params = parse_qs(self.path[delim_idx+1:])
        self.validate(path, params)
        return path, params

    def validate(self, path, params):
        self.validate_path()
        self.validate_params()

    def validate_path(self):
        pass

    def validate_params(self):
        pass

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
