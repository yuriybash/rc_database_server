from BaseHTTPServer import BaseHTTPRequestHandler
from storage import InMemoryStorage
from urlparse import parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    STORAGE = InMemoryStorage()

    def do_GET(self):
        path, params = self.parse()

        if(path == 'set'):
            self.STORAGE.store_multiple(params)
        elif(path == 'get'):
            return self.STORAGE.retrieve(params['key'])
        else:
            raise ValueError("%s is an invalid path, please try again" % path)

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
