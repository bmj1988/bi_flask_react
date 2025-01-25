import time
import pandas as pd
from flask import current_app
from pathlib import Path
from app.services.extract_signature_info import extract_signature_info
from app.services.tiered_search import tiered_search
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

def process_single_page(image_path: Path, app) -> List[Dict]:
    with app.app_context():
        try:
            page = int(image_path.stem.split('page-')[-1])
            resulting_data = extract_signature_info(image_path)

            matched_list = []
            for idx, dict_ in enumerate(resulting_data):
                name_, score_, id_ = tiered_search(dict_)
                if name_ == '':
                    continue

                temp_dict = {
                    "OCR_RECORD": f"{dict_['Name']} {dict_['Address']}",
                    "MATCHED_RECORD": name_,
                    "SCORE": "{:.2f}".format(score_),
                    "VALID": score_ > 85.0,
                    "PAGE": page,
                    "ROW": idx + 1
                }
                matched_list.append(temp_dict)

            return matched_list

        except Exception as e:
            print(f"Error processing page {image_path.stem}: {str(e)}")
            return []

def perform_database_crosscheck() -> tuple[List[Dict], int, int, float]:

    start_time = time.time()
    app = current_app._get_current_object()  # Get the actual app object

    # Get all jpg files
    jpg_files = list(Path(current_app.config['UPLOAD_FOLDER']).glob('*.jpg'))
    if not jpg_files:
        print("No images provided for database cross-check.")
        return [], 0, 0, 0.0

    # Calculate optimal workers for this system
    max_workers = int(os.getenv('MAX_WORKERS', '1'))
    print(f"Processing with {max_workers} workers")

    matched_list = []

    # Process images in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks with app context
        future_to_path = {
            executor.submit(process_single_page, path, app): path
            for path in jpg_files
        }

        # Process results as they complete
        completed_pages = 0
        total_pages = len(jpg_files)

        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                results = future.result()
                matched_list.extend(results)

                # Update progress
                completed_pages += 1
                progress = (completed_pages / total_pages) * 100
                print(f"Progress: {completed_pages}/{total_pages} pages ({progress:.1f}% -- Time: {time.time() - start_time:.3f} seconds)")

            except Exception as e:
                print(f"Failed to process {path.stem}: {str(e)}")

    # Create DataFrame from results
    voter_record_ocr_matches = pd.DataFrame(
        matched_list,
        columns=["OCR_RECORD", "MATCHED_RECORD", "SCORE", "VALID", "PAGE", "ROW"]
    ).sort_values(by=['PAGE', 'ROW'])

    end_time = time.time()
    total_time = end_time - start_time
    total_records = len(voter_record_ocr_matches)
    valid_matches = voter_record_ocr_matches["VALID"].sum()

    print(f"Processing completed in {total_time:.3f} seconds")
    print(f"Found {valid_matches} valid matches out of {total_records} total records")

    return [
        voter_record_ocr_matches.to_dict(orient='records'),
        total_records,
        valid_matches,
        total_time
    ]
