from flask import Blueprint

record_blueprint = Blueprint("record_blueprint", __name__)
from . import views
