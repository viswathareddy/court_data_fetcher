from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    # Basic config: update/database URI as needed
    app.config['SECRET_KEY'] = 'change_this_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///court_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Add configuration for URL building outside request context
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    db.init_app(app)

    # Import routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
