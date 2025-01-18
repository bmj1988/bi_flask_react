import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'pdf', 'csv'}
    CSV_FILE_PATH = 'data/voter_records.csv'
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# To switch configurations, set the FLASK_DEBUG environment variable
config = {
    'debug': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Function to get the configuration based on the FLASK_DEBUG environment variable
def get_config():
    flask_debug = os.environ.get('FLASK_DEBUG', '1')
    return config['debug'] if flask_debug == '1' else config['production']
