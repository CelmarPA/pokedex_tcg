# app/progress/__init__.py
from flask import Blueprint


progress: Blueprint = Blueprint("progress", __name__)


from . import routes