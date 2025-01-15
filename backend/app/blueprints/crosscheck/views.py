from flask import jsonify, current_app
import os
from pdf2image import convert_from_bytes
from app.services.voter_records_crosscheck import perform_database_crosscheck

def crosscheck(request):
    if 'pdf_files' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_files = request.files.getlist('pdf_files')
    images = None

    for pdf_file in pdf_files:
        if pdf_file.filename == '' or not pdf_file.filename.endswith('.pdf'):
            return jsonify({"error": "Invalid file provided"}), 400

        try:
            # Save PDF to the specified folder
            pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Convert PDF to images using pdf2image
            with open(pdf_path, 'rb') as f:
                images = convert_from_bytes(f.read())

            # Save each image as a JPEG
            for i, image in enumerate(images):
                image.save(f"{current_app.config['UPLOAD_FOLDER']}/{pdf_file.filename}-page-{i:02d}.jpg")

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    [voter_record_ocr_matches, total_records, valid_matches, total_time] = perform_database_crosscheck(images)  # Perform the database cross-check

    return jsonify({"voter_record_ocr_matches": voter_record_ocr_matches, "total_records": total_records, "valid_matches": valid_matches, "total_time": total_time})

def wipe_uploads():
    # Clear the uploads folder
    for file in os.listdir(current_app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file))
    return jsonify({"cleared": True})