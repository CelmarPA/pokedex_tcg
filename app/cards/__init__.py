# app/cards/__ini__.py
from flask import Blueprint


cards: Blueprint = Blueprint("cards", __name__)


from . import routes