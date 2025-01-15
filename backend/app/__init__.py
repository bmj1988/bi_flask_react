from flask import Flask
import pandas as pd
import os
from app.blueprints import register_blueprints
from config import get_config

# Function to load the CSV file (or create an empty dataframe if it doesn't exist)
def load_voter_records(app):
    csv_path = app.config.get('CSV_FILE_PATH')

    if os.path.exists(csv_path):
        try:
            records = pd.read_csv(csv_path)
            records['Full Name'] = records["First_Name"] + ' ' + records['Last_Name']
            records['Full Address'] = (records["Street_Number"] + " " +
                                     records["Street_Name"] + " " +
                                     records["Street_Type"] + " " +
                                     records["Street_Dir_Suffix"])
            records['Full Name and Full Address'] = records["Full Name"] + ' ' + records["Full Address"]
            app.logger.info(f"Data loaded from {csv_path}")
            return records
        except Exception as e:
            app.logger.error(f"Error loading CSV: {e}")
            return pd.DataFrame()
    else:
        app.logger.warning("No CSV found. Initialized an empty voter_records.")
        return pd.DataFrame()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(get_config())

    # Register blueprints
    register_blueprints(app)

    # Load voter records and attach to app
    app.voter_records = load_voter_records(app)

    return app

# Create the app instance
app = create_app()
