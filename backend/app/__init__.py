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
            # Use chunksize to read the file in chunks
            chunks = []
            for chunk in pd.read_csv(csv_path, chunksize=10000):
                # Process each chunk
                chunk['Full Name'] = chunk["First_Name"].astype(str) + ' ' + chunk['Last_Name'].astype(str)
                chunk['Full Address'] = (chunk["Street_Number"].astype(str) + " " +
                                       chunk["Street_Name"].astype(str) + " " +
                                       chunk["Street_Type"].astype(str) + " " +
                                       chunk["Street_Dir_Suffix"].astype(str))
                chunk['Full Name and Full Address'] = chunk["Full Name"].astype(str) + ' ' + chunk["Full Address"].astype(str)
                chunk['WARD'] = chunk['WARD'].apply(clean_ward)
                chunks.append(chunk)

            # Combine all chunks
            records = pd.concat(chunks, ignore_index=True)
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
    # Get frontend URL from environment variable, with deployed URL as fallback
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://bi-frontend-app.onrender.com")

    cors_options = {
        "origins": [FRONTEND_ORIGIN],  # Explicitly allow only the frontend origin
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers"
        ],
        "expose_headers": [
            "Content-Length",
            "Content-Range"
        ]
    }
    # Allow only frontend origin in production, all origins in development
    CORS(app, resources={r"/*": cors_options})

    # Load configuration
    app.config.from_object(get_config())

    # Register blueprints
    register_blueprints(app)

    # Load voter records and attach to app
    app.voter_records = load_voter_records(app)

    return app

# Create the app instance
app = create_app()
