# app/activity/__init__.py
from flask import Blueprint


activity: Blueprint = Blueprint("activity", __name__)


from . import routes
