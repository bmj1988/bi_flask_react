from app import create_app

# Initialize the Flask app using a factory function pattern
app = create_app()

if __name__ == "__main__":
    # Run the Flask app on the default port 5000 with debug mode enabled
    app.run(host='0.0.0.0', port=5000, debug=True)
