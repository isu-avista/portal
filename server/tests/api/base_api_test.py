import os
import unittest
from tests.mock_service import MockService
from pathlib import Path
from dotenv import load_dotenv
import avista_data


class BaseApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        while not os.path.isdir("test-data"):
            os.chdir("..")
        basedir = Path(os.getcwd()).absolute() / "test-data"
        cls.write_env_file(basedir, "test.env")
        load_dotenv(os.path.join(basedir, 'test.env'))

    @classmethod
    def write_env_file(cls, basedir, file):
        with open(basedir / file, "w") as f:
            f.write("CONFIG_PATH=" + (basedir / 'conf').__str__() + "\n")
            f.write("LOG_PATH=" + (basedir / 'logs').__str__())

    def setUp(self):
        self.server = MockService.get_instance()
        self.server.initialize()
        self.server.start()
        self.client = self.server._app.test_client()

    def tearDown(self):
        avista_data.database.clear_data()
        self.server.stop()

    @staticmethod
    def __login(client, email, password):
        return client.post('/api/login', json=dict(
            email=email,
            password=password
        ))

    @staticmethod
    def _create_auth_header(client, email, password):
        credentials = BaseApiTest.__login(client, email, password)
        return {
            'Authorization': f'Bearer {credentials.get_json()["token"]}'
        }

    @staticmethod
    def auth_get(client, email, password, route):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.get(route, headers=headers)

    @staticmethod
    def auth_post(client, email, password, route, json):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.post(route, headers=headers, json=json)

    @staticmethod
    def auth_put(client, email, password, route, json):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.put(route, headers=headers, json=json)

    @staticmethod
    def auth_delete(client, email, password, route):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.delete(route, headers=headers)


if __name__ == '__main__':
    unittest.main()
