# app/achievement/__init__.py

from flask import Blueprint


achievement: Blueprint = Blueprint("achievement", __name__)


from . import routes
