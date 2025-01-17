import time
import pandas as pd
from flask import current_app
from pathlib import Path
from app.services.extract_signature_info import extract_signature_info
from app.services.tiered_search import tiered_search

def perform_database_crosscheck():
    #Performs the database cross-check and returns a DataFrame with results.
    matched_list = []
    start_time = time.time()

    # Path where images are stored
    jpg_files = Path(current_app.config['UPLOAD_FOLDER']).glob('*.jpg')

    if not jpg_files:
        print("No images provided for database cross-check.")
        return pd.DataFrame()  # Return an empty DataFrame if no images are provided

    # Process each image file
    for image_path in jpg_files:
        # Extract signature information using the provided function
        resulting_data = extract_signature_info(image_path)

        # Perform name matching and build results
        for dict_ in resulting_data:
            name_, score_, id_ = tiered_search(dict_)
            if name_ == '':
                continue

            # Build the result dictionary
            temp_dict = {
                "OCR_RECORD": f"{dict_['Name']} {dict_['Address']}",
                "MATCHED_RECORD": name_,
                "SCORE": "{:.2f}".format(score_),
                "VALID": score_ > 85.0
            }
            matched_list.append(temp_dict)

        # Print progress in the console instead of a progress bar

    # Create a DataFrame from the results
    voter_record_ocr_matches = pd.DataFrame(matched_list, columns=["OCR_RECORD", "MATCHED_RECORD", "SCORE", "VALID"])

    end_time = time.time()
    total_records = len(voter_record_ocr_matches)
    valid_matches = voter_record_ocr_matches["VALID"].sum()
    total_time = end_time - start_time

    # Print results to the console
    print(f"OCR and Match Time: {end_time-start_time:.3f} secs")
    print(f"Number of Matched Records: {valid_matches} out of {total_records}")

    return [voter_record_ocr_matches.to_dict(orient='records'), total_records, valid_matches, total_time]
