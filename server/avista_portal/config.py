import os


class Config(object):
    """ A Configuration object

    Note that this object needs to replaced with configuration read in from yaml using
    the avista_base_server config reader

    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = 'TEST_KEY'
    JWT_SECRET_KEY = 'TEST_KEY'
