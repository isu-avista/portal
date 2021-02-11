""" This package contains the modules containing the route logic for the service """
from flask import Blueprint

api_bp = Blueprint('portal_api', __name__)

from avista_portal.api import data
