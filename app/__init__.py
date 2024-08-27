import os

from flask import Flask
from app.utils.db import db, migrate
from app.routes.fund_route import fund_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLITE_DATABASE_URL') or 'sqlite:///development.db'
    
    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Routes
    app.register_blueprint(fund_bp)
    
    return app
