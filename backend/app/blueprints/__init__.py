# Import all blueprints
from app.blueprints.crosscheck import crosscheck_bp
from app.blueprints.voter_records import voter_records_bp

# List of all blueprints to be registered with the app
all_blueprints = [
    crosscheck_bp,
    voter_records_bp,
]

# Function to register all blueprints
def register_blueprints(app):
    # Register all blueprints with the app
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
