import os
import sys
from wsgiref import simple_server
from simple_framework.main import Framework

from urls import routes, fronts


app = Framework(routes, fronts)

if __name__ == "__main__":
    # Get the path and port from command-line arguments
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    # Make and start the server until control-c
    httpd = simple_server.make_server("", port, app)
    print(f"Serving {path} on port {port}, control-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()

# with simple_server.make_server('', 8080, app) as httpd:
#     print("Запуск на порту 8080...")
#     httpd.serve_forever()

