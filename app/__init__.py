import os

from flask import Flask
from app.utils.db import db
from app.routes.fund_route import fund_bp
from config import DevelopmentConfig, TestConfig

CONFIG_CLASSES = {
    'development': DevelopmentConfig,
    'testing': TestConfig
}

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    config_class = CONFIG_CLASSES.get(env)

    if config_class:
        app.config.from_object(config_class)
    else:
        raise ValueError(f"Invalid FLASK_ENV value: {env}")
    
    # Initialize DB
    db.init_app(app)
    
    # Register Routes
    app.register_blueprint(fund_bp)
    
    return app
