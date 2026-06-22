# app/wishlist/__init__.py
from flask import Blueprint


wishlist: Blueprint = Blueprint("wishlist", __name__)


from . import routes
