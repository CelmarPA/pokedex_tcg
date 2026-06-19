# app/favorite/__init__.py
from flask import Blueprint


favorite: Blueprint = Blueprint("favorite", __name__)


from . import routes
