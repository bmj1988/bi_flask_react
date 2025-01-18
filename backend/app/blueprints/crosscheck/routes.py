from flask import request
from app.blueprints.crosscheck import crosscheck_bp
from app.blueprints.crosscheck.views import crosscheck, wipe_uploads

@crosscheck_bp.route('/crosscheck', methods=['POST'])
def crosscheck_route():
    return crosscheck(request)

@crosscheck_bp.route('/wipe_uploads', methods=['POST'])
def wipe_uploads_route():
    return wipe_uploads()
