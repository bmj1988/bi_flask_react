from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configurations from config.py
    app.config.from_object('config')

    # Register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
