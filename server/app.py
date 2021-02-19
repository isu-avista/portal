from dotenv import load_dotenv

from avista_portal.server import PortalServer
from avista_base.avista_app import AvistaApp
from pathlib import Path
import os
import socket


def get_ipaddress():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(10)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except socket.error:
        return "0.0.0.0"


# configuration
DEBUG = True

path = Path(os.getcwd()) / ".flaskenv"
if path.exists():
    load_dotenv(path)

if __name__ == '__main__':
    service = PortalServer.get_instance()
    service.initialize()
    service.start()
    app = service.get_app()
    options = dict(
        bind=f'{get_ipaddress()}:{service.get_port()}',
        workers=1
    )
    AvistaApp(app, options).run()
