from flask import Blueprint

friend_blueprint = Blueprint("friend_blueprint", __name__)

from . import views