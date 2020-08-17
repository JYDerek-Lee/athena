from flask import Blueprint

public_api: Blueprint = Blueprint("public_api", __name__)

from .v1.slack import *
