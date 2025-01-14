import pandas as pd
import os

def load_dataframe(file_path='data/sample_data.csv'):
    """
    Loads the pandas DataFrame from a CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")
    return pd.read_csv(file_path)

dataframe = load_dataframe()
