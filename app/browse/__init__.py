from flask import Blueprint

browse_bp = Blueprint(
    "browse_bp", __name__, template_folder="app/templates", static_folder="app/static"
)

from . import routes
    