from flask import Flask
import pandas as pd
import os
from app.blueprints import register_blueprints
from config import get_config
from flask_cors import CORS

def clean_ward(ward_value):
    try:
        # Convert to float first, then to int to handle the decimal format
        return int(float(ward_value))
    except (ValueError, TypeError):
        # Return None or some default value if conversion fails
        return None

# Function to load the CSV file (or create an empty dataframe if it doesn't exist)
def load_voter_records(app):
    csv_path = app.config.get('CSV_FILE_PATH')

    if os.path.exists(csv_path):
        try:
            records = pd.read_csv(csv_path)
            records['Full Name'] = records["First_Name"].astype(str) + ' ' + records['Last_Name'].astype(str)
            records['Full Address'] = (records["Street_Number"].astype(str) + " " +
                                     records["Street_Name"].astype(str) + " " +
                                     records["Street_Type"].astype(str) + " " +
                                     records["Street_Dir_Suffix"].astype(str))
            records['Full Name and Full Address'] = records["Full Name"].astype(str) + ' ' + records["Full Address"].astype(str)
            records['WARD'] = records['WARD'].apply(clean_ward)
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

    # Enable CORS
    # Get frontend URL from environment variable (for Docker support)
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

    # Allow only frontend origin in production, all origins in development
    CORS(app, resources={r"/*": {"origins": FRONTEND_ORIGIN}})

    # Load configuration
    app.config.from_object(get_config())

    # Register blueprints
    register_blueprints(app)

    # Load voter records and attach to app
    app.voter_records = load_voter_records(app)

    return app

# Create the app instance
app = create_app()
