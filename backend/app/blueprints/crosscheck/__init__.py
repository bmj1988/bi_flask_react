from flask import Blueprint

crosscheck_bp = Blueprint('crosscheck', __name__)

from app.blueprints.crosscheck import routes
