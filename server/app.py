from dotenv import load_dotenv

from avista_portal.server import PortalServer
from pathlib import Path
import os

# configuration
DEBUG = True


path = Path(os.getcwd()) / ".flaskenv"
if path.exists():
    load_dotenv(path)

if __name__ == '__main__':
    PortalServer.get_instance().init()
    PortalServer.get_instance().start()
