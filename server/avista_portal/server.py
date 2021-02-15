from avista_base.service import Service
import avista_portal.api as api


class PortalServer(Service):
    """ A Singleton instance for the IoT server

    Note that this class should extend the server class from avista_base_server while keeping
    the singleton characteristics. Basically, we need to merge in the capabilities of this class
    with those of the base_server.server class.

    """
    def __init__(self):
        """ instantiate the app """
        super().__init__()

    def _setup_endpoints(self):
        super()._setup_endpoints()
        self._app.register_blueprint(api.api_bp)

    def start(self):
        super().start()


    def check_status(self):
        pass
