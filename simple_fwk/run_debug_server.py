import os
import sys
from pathlib import Path
from wsgiref import simple_server

from fwk.main import DebugApplication
from fwk.middleware import middlewares
from views import urlpatterns

BASE_DIR = Path.cwd().resolve()
TEMPLATES = '/templates/'
STATIC = '/static/'

settings = {
    'BASE_DIR': str(BASE_DIR),
    'TEMPLATES': TEMPLATES,
    'TEMPLATES_ROOT': str(BASE_DIR / TEMPLATES[1:-1]),
    'STATIC': STATIC,
    'STATIC_ROOT': str(BASE_DIR / STATIC[1:-1]),
}

app = DebugApplication(urls=urlpatterns, settings=settings, middlewares=middlewares)


if __name__ == "__main__":
    # Get the path and port from command-line arguments
    path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    # Make and start the server until control-c
    httpd = simple_server.make_server("", port, app)
    print(f"Debug Serving {path} on port {port}, control-C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()
