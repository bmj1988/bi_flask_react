from rapidfuzz import process, fuzz, utils
import numpy as np
import pandas as pd
from flask import current_app

def score_fuzzy_match_slim(ocr_name, full_name_list, scorer_=fuzz.token_ratio, limit_=1):
    list_of_match_tuples = process.extract(query=ocr_name, choices=full_name_list, scorer=scorer_, processor=utils.default_process, limit=limit_)
    return list_of_match_tuples

def tiered_search(_dict):
    name, address, ward = _dict['Name'], _dict['Address'], _dict['Ward']
    name_address_combo = f"{name} {address}"
    print('!!!Tiered Search', name, address, ward, _dict)
    voter_records = current_app.voter_records

    # Searches for a match within the Ward returned by OCR
    try:
        ward_int = int(ward)
        name_address_matches1 = score_fuzzy_match_slim(
            name_address_combo,
            voter_records[voter_records['WARD'].notna() & (voter_records['WARD'] == ward_int)]["Full Name and Full Address"]
        )
    except (ValueError, TypeError):
        name_address_matches1 = []

    if len(name_address_matches1) == 0:
        return '', 0.0, 0

    name_address__name1, name_address__score1, name_address__id1 = name_address_matches1[0]

    # if score is more than 85, return the tuple
    if name_address__score1 >= 85.0:
        return (name_address__name1, name_address__score1, name_address__id1)

    # if score is below 85, do additional processing
    else:

        # computing matches based on name and address; only considers all other wards
        name_address_matches2 = score_fuzzy_match_slim(name_address_combo, voter_records[voter_records['WARD'] != f"{ward}.0"]["Full Name and Full Address"])
        name_address__name2, name_address__score2, name_address__id2 = name_address_matches2[0]

        # if the new voter records score is greater than 85, return tuple
        if name_address__score2 >= 85.0:
            return (name_address__name2, name_address__score2, name_address__id2)

        # if score is less than 85, perform full records search based on name
        # and return results with highest score
        else:
            # computing matches based on name alone; considers full voter records
            full_name_matches = score_fuzzy_match_slim(name, voter_records["Full Name"], scorer_=fuzz.ratio)
            full_name__name, full_name__score, full_name__id = full_name_matches[0]

            # find max from three scores
            max_indx = np.argmax([name_address__score1, name_address__score2, full_name__score])

            # return records associated with that max
            if max_indx== 0:
                return (name_address__name1, name_address__score1, name_address__id1)
            elif max_indx == 1:
                return (name_address__name2, name_address__score2, name_address__id2)
            else:
                address = voter_records.loc[full_name__id, 'Full Address']
                full_name_address = f"{full_name__name} {address}"
                return (full_name_address, full_name__score, full_name__id)
