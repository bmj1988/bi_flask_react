from flask import Blueprint, request, jsonify
from app.models import dataframe

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@main_bp.route('/', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # if file and allowed_file(file.filename):
    #     try:
            # reader = PyPDF2.PdfReader(file)
            # content = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            # # Example of cross-checking data
            # match_found = any(dataframe['column_name'].str.contains(content))
            # return jsonify({'match_found': match_found})
        # except Exception as e:
        #     return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400
