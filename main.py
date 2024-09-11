from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
import os

from config import Config
from models import db, User
from auth import auth_bp
from job_matching import job_matching_bp
from automated_application import automated_application_bp
from admin import admin_bp
from openai_chat_completion.chat_request import test_openai_integration

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(job_matching_bp)
app.register_blueprint(automated_application_bp)
app.register_blueprint(admin_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_openai')
def test_openai():
    result = test_openai_integration()
    return result

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Initialize and start the background scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    app.run(host='0.0.0.0', port=5000)
