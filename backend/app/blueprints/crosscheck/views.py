from flask import jsonify, current_app
import os
from pdf2image import convert_from_bytes
from app.services.voter_records_crosscheck import perform_database_crosscheck
from PIL import Image

def crosscheck(request):
    if 'imageData' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    uploaded_files = request.files.getlist('imageData')
    pdf_images = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename == '':
            return jsonify({"error": "Invalid file provided"}), 400

        file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
        if file_ext not in ['.pdf', '.jpg', '.jpeg']:
            return jsonify({"error": "Invalid file type. Only PDF and JPG/JPEG files are allowed"}), 400

        try:
            if file_ext == '.pdf':
                # Handle PDF files
                pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(pdf_path)

                # Convert PDF to images
                with open(pdf_path, 'rb') as f:
                    pdf_images.extend(convert_from_bytes(f.read()))

                # Save each image from PDF
                pdf_file_name = os.path.splitext(uploaded_file.filename)[0]
                for i, image in enumerate(pdf_images):
                    image_path = f"{current_app.config['UPLOAD_FOLDER']}/{pdf_file_name}-page-{i+1:02d}.jpg"
                    image.save(image_path)
            else:
                # Handle JPG/JPEG files directly
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{uploaded_file.filename}-page-{i+1:02d}.jpg")
                uploaded_file.save(image_path)
                # Add the image to our list (as PIL Image object for consistency)
                pdf_images.append(Image.open(image_path))

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    [voter_record_ocr_matches, total_records, valid_matches, total_time] = perform_database_crosscheck()

    return jsonify({
        "voter_record_ocr_matches": voter_record_ocr_matches,
        "total_records": int(total_records),
        "valid_matches": int(valid_matches),
        "total_time": total_time,
        "total_pages": len(pdf_images)
    })

def wipe_uploads():
    # Clear the uploads folder
    for file in os.listdir(current_app.config['UPLOAD_FOLDER']):
        if file != '.gitkeep':
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file))
    return jsonify({"cleared": True})
