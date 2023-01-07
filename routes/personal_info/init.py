from flask import Blueprint

personal_info_blueprint = Blueprint("personal_info_blueprint", __name__)

from . import views
