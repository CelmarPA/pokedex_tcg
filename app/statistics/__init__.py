# app/statistics/__init__.py
from flask import Blueprint


statistics: Blueprint = Blueprint("statistics", __name__)


from . import routes
