from flask import Blueprint


login_bp = Blueprint(
    "login_bp", __name__, template_folder="app/templates", static_folder="app/static"
)

from . import routes
    