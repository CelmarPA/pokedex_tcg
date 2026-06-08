# app/auth/__init__.py
from flask import Blueprint


auth: Blueprint = Blueprint("auth", __name__)


print("Auth Registered")
