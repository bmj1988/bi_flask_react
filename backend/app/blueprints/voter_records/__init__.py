from flask import Blueprint

voter_records_bp = Blueprint('voter_records', __name__)

from app.blueprints.voter_records import routes
