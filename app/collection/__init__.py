# app/collection/__init__.py
from flask import Blueprint

collection: Blueprint = Blueprint("collection", __name__)

from . import routes
