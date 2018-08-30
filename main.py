import sys
from BaseHTTPServer import HTTPServer
from handlers import RequestHandler

DEFAULT_PORT = 4000

def run_server():
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    address = ('127.0.0.1', port)
    httpd = HTTPServer(address, RequestHandler)
    print('Starting server on port %d' % port)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
