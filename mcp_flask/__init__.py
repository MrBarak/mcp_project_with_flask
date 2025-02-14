from flask import Flask
from flask_session import Session
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    
    # Session configuration
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    Session(app)

    # Register API routes
    app.register_blueprint(api_bp, url_prefix="/api/mcp")

    return app
