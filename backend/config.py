import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'pdf'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# To switch configurations, set the FLASK_ENV environment variable
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
