from avista_portal.server import PortalServer
from multiprocessing import Process


class MockService(PortalServer):

    def __init__(self):
        """ instantiate the app """
        super().__init__()

    def start(self):
        super().start()
        self._proc = Process(target=self._app.run, kwargs={'host': self.hostname, 'port': self.port})
        self._proc.start()
