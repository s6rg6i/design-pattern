from wsgiref.simple_server import make_server

""" https://docs.python.org/3/library/wsgiref.html#examples
Every WSGI application must have an application object - a callable object that accepts two arguments.
For that purpose, we're going to use a function (note that you're not limited to a function, you can
use a class for example). The first argument passed to the function is a dictionary containing CGI-style
environment variables and the second variable is the callable object.
"""


def application(environ, start_response):
    status = "200 OK"  # HTTP Status
    headers = [("Content-type", "text/plain; charset=utf-8")]  # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b'Hello world from a simple WSGI application!', b'next string']


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()  # Serve until process is killed
