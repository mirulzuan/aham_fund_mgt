import os

from flask import Flask
from app.utils.db import db, migrate
from app.routes.fund_route import fund_bp
from config import DevelopmentConfig, TestConfig, MigrationConfig

CONFIG_CLASSES = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'migration': MigrationConfig
}

def create_app(env='development'):
    app = Flask(__name__)
    config_class = CONFIG_CLASSES.get(env)

    if config_class:
        app.config.from_object(config_class)
    else:
        raise ValueError(f"Unsupported env: {env}")
    
    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Routes
    app.register_blueprint(fund_bp)
    
    return app
