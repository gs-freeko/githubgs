from flask import Flask
from app.routes.aggregator import aggregator_bp
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(aggregator_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")

    return app
