from flask import jsonify, current_app
import pandas as pd
import os

#Splash page to check if the dataframe is empty
def splash():
    dataframe_empty = current_app.voter_records.empty
    # Check if any files except .gitkeep exist in the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_folder)
    pdf_loaded = any(f != '.gitkeep' for f in files)
    return jsonify({"dataframeEmpty": dataframe_empty, "pdfLoaded": pdf_loaded})

# Upload CSV file to the dataframe
def upload_csv(request):
    from app import load_voter_records
    if 'csv_file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    csv_file = request.files['csv_file']

    if csv_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not csv_file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400

    try:
        # Directly save the uploaded file
        csv_file.save(current_app.config['CSV_FILE_PATH'])
        # Reload the voter records after saving
        current_app.voter_records = load_voter_records(current_app)
        return jsonify({"message": f"CSV uploaded and saved to {current_app.config['CSV_FILE_PATH']}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Clear the dataframe
def clear_data():
    current_app.voter_records = pd.DataFrame()  # Clear the in-memory DataFrame
    if os.path.exists(current_app.config['CSV_FILE_PATH']):
        os.remove(current_app.config['CSV_FILE_PATH'])
    return jsonify({"message": "Data cleared successfully."})
