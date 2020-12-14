from avista_portal.server import PortalServer


# configuration
DEBUG = True

app = PortalServer.get_instance().app


if __name__ == '__main__':
    PortalServer.get_instance().start()