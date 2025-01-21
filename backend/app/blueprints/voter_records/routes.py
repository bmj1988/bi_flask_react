from flask import request, jsonify
from app.blueprints.voter_records import voter_records_bp
from app.blueprints.voter_records.views import splash, upload_csv, clear_data

@voter_records_bp.route('/splash', methods=['GET'])
def splash_route():
    return splash()

@voter_records_bp.route('/upload_csv', methods=['POST'])
def upload_csv_route():
    return upload_csv(request)

@voter_records_bp.route('/clear_csv', methods=['POST'])
def clear_data_route():
    return clear_data()

@voter_records_bp.route('/health', methods=['GET'])
def health_route():
    return jsonify({"status": "ok"}), 200
