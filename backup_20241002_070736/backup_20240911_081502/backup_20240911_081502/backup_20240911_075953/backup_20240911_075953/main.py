import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from auth import auth_bp
from job_matching import job_matching_bp
from automated_application import automated_application_bp
from admin import admin_bp
import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(job_matching_bp)
app.register_blueprint(automated_application_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_openai')
def test_openai():
    from openai_chat_completion.chat_request import test_openai_integration
    return test_openai_integration()

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Starting the application')
    
    # Initialize the database
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {str(e)}')
    
    # Run the app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
