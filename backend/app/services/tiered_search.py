from rapidfuzz import process, fuzz, utils
import numpy as np
import pandas as pd
from flask import current_app

CONFIDENCE_THRESHOLD = 85.0

def score_fuzzy_match_slim(ocr_name, full_name_list, scorer_=fuzz.token_ratio, limit_=1):
    list_of_match_tuples = process.extract(query=ocr_name, choices=full_name_list, scorer=scorer_, processor=utils.default_process, limit=limit_)
    return list_of_match_tuples

def tiered_search(record_dict: dict) -> tuple[str, float, int]:

    name, address, ward = record_dict['Name'], record_dict['Address'], record_dict['Ward']
    search_text = f"{name} {address}"
    voter_records = current_app.voter_records

    # First tier: Search within the specified ward
    try:
        ward_int = int(ward)
        ward_matches = score_fuzzy_match_slim(
            search_text,
            voter_records[voter_records['WARD'] == ward_int]["Full Name and Full Address"]
        )
        if ward_matches and ward_matches[0][1] >= CONFIDENCE_THRESHOLD:
            return ward_matches[0]
    except (ValueError, TypeError):
        pass

    # Second tier: Search all other wards
    other_wards_matches = score_fuzzy_match_slim(
        search_text,
        voter_records["Full Name and Full Address"]
    )
    if other_wards_matches and other_wards_matches[0][1] >= CONFIDENCE_THRESHOLD:
        return other_wards_matches[0]

    # Third tier: Search by name only across all records
    name_only_matches = score_fuzzy_match_slim(
        name,
        voter_records["Full Name"],
        scorer_=fuzz.ratio
    )

    if name_only_matches:
        matched_id = name_only_matches[0][2]
        matched_address = voter_records.loc[matched_id, 'Full Address']
        return (
            f"{name_only_matches[0][0]} {matched_address}",
            name_only_matches[0][1],
            matched_id
        )

    # If no matches found at all
    return ('', 0.0, 0)
