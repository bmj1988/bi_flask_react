# Ballot Initiative Crosscheck ApplicationBackend Server

This is a Flask-based backend server that handles CSV file processing and provides API endpoints.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

 - On Windows, use `venv\Scripts\activate`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
FLASK_APP=app
FLASK_ENV=development
FRONTEND_ORIGIN=http://localhost:3000  # Change this in production
OPENAI_API_KEY=your_openai_api_key
```

## Running the Server

1. For development:
```bash
python run.py
```
The server will start at `http://localhost:5000`

## API Endpoints

- `POST /upload_csv`: Upload and process CSV files
  - Accepts: multipart/form-data with a CSV file
  - Returns: JSON response with processing status

- `GET /splash`: Checks to see if a CSV is uploaded and whether or not there are temp files in the uploads folder
  - Returns: JSON response with dataframeEmpty (BOOLEAN) and pdfLoaded (BOOLEAN) values

- `POST /clear_csv`: Clears the CSV file used for processing.
  - Returns: JSON response with processing status

- `POST /wipe_uploads`: Clears the uploads folder.
  - Returns: JSON response with processing status

- `POST /crosscheck`: Runs the crosscheck process.
  - Accepts: multipart/form-data with PDF files
  - Returns: JSON response with processing status

## Development Notes

- The server uses CORS to allow requests from the frontend origin specified in FRONTEND_ORIGIN
- CSV files are processed in chunks to manage memory usage
- Debug logging is enabled in development mode

## Deployment

When deploying:
1. Set FRONTEND_ORIGIN to your production frontend URL
2. Set FLASK_ENV to 'production'
3. Ensure adequate memory allocation for CSV processing. 2GB RAM is sufficient.

## Error Handling

The server logs errors to help debug issues:
- CSV processing errors
- Memory usage warnings
- CORS configuration details

## Requirements

See `requirements.txt` for a full list of dependencies. Key packages include:
- Flask
- pandas
- flask-cors
- openai
- rapidfuzz
- numpy
- pdf2image


## Issues:

* **CSV Column Flexibility:**
  To make the process truly universal, the vectorized columns used for crosscheck would have to be dynamically generated based on the CSV being used for the voter records. This would require a more complex backend setup.

* **Server Architecture:**
  Flask is not the best choice for a production server for a centralized application. It is not designed for high concurrency and is not scalable. Given that this project seems to work ideally as a local application with the stakeholder's API key, it is not a pressing concern at this time. If the presiding sentiment in the future is that the app should be centralized, then it would be worth the effort to set up a more robust backend.

* **Security:**
  Routes are not protected by authentication. This is a security risk and should be addressed in the future.

* **Performance & Compatibility:**
  The crosscheck process is not fully optimized. It takes a long time to run and is not scalable. The process should be optimized and parallelized to handle large amounts of data. Furthermore, the process should be able to handle image formats other than PDF in the event that, say, a mobile user wishes to upload a picture of petition from their phone.
