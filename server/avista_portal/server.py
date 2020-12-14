import avista_data as data
from avista_base import config as conf
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from pathlib import Path
from avista_portal.config import Config
from avista_portal import api
from avista_data.user import User
import os
import logging
from multiprocessing import Process


class PortalServer:
    """ A Singleton instance for the IoT server

    Note that this class should extend the server class from avista_base_server while keeping
    the singleton characteristics. Basically, we need to merge in the capabilities of this class
    with those of the base_server.server class.

    """
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method

        Returns:
            The singleton instance of IoTServer
        """
        if PortalServer.__instance is None:
            PortalServer()
        return PortalServer.__instance

    def __init__(self):
        """ instantiate the app """
        if PortalServer.__instance is not None:
            raise Exception("This class is a singletion!")
        else:
            PortalServer.__instance = self
            self.proc = None
            self.app = Flask(__name__)
            self.app.config.from_object(Config())
            self.app.app_context().push()
            self.config = {}
            self.configfile = Path(os.getcwd()) / "conf" / "config.yml"
            print("Config File: " + str(self.configfile))
            self.logfile = Path(os.getcwd()) / "logs" / "server.log"

            # enable CORS
            CORS(self.app, resources={r"/*": {"origins": "*"}})
            self.jwt = JWTManager(self.app)

            data.data_manager.init()
            data.data_manager.get_db().create_all()
            data.populate_initial_data()

            self.app.register_blueprint(api.api_bp)

            @self.jwt.user_claims_loader
            def add_claims_to_access_token(identity):
                user = User.find_user(identity)
                return {'role': str(user.get_role())}

    def start(self):
        """ starts the server """
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG)
        self.config = conf.load(self.configfile)
        self.proc = Process(target=self.app.run)
        self.proc.start()

    def stop(self):
        """ Stops the server """
        self.proc.terminate()
        self.proc.join()

    def get_config(self, section):
        """ retrieves the config for the given section

        Args:
            section (str): The name of the section of the config to retrieve

        Returns:
            a dictionary representing the subsection of the configuration

        Raises:
            Exception if the provided section is None, empty, or non-existant
        """
        if section is None or section == "" or section not in self.config.keys():
            raise Exception("section cannot be None or empty and must be in the config")
        return self.config[section]

    def set_config(self, section, config_data):
        """ Updates the config section with the provided configuration information

        Args:
            section (str): the section to update

            config_data (dict): the new data for the section

        Raises:
            Exception if the provided section is None or empty or the provided data is None
        """
        if section is None or section == "":
            raise Exception("section cannot be None or empty")
        if config_data is None:
            raise Exception("data cannot be None")
        self.config[section] = config_data
        conf.save(self.config, self.configfile)

    def check_status(self):
        pass

    def get_log(self):
        """ returns the last five lines of the log

        Returns:
            a dictionary containing a single entry "log" which is the last five lines of the log file
        """
        with open(self.logfile, "r") as a_file:
            lines = a_file.readlines()
            return dict(log='\n'.join(lines[-5:]))
