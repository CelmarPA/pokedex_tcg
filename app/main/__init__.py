# app/main/__init__.py
from flask import Blueprint


main: Blueprint = Blueprint("main", __name__)


print("Main Registered")
