from flask import Blueprint

rank_blueprint = Blueprint("rank_blueprint", __name__)

from . import views
