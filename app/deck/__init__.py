# app/deck/__init__.py

from flask import Blueprint


deck: Blueprint = Blueprint("deck", __name__)


from . import routes
