from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
import os
import ssl
from threading import Thread

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

def run_app(ssl_context=None):
    if ssl_context:
        app.run(host='0.0.0.0', port=5000, ssl_context=ssl_context, debug=True, use_reloader=False)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Initialize and start the background scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    # SSL context
    try:
        cert_path = os.path.abspath('cert.pem')
        key_path = os.path.abspath('key.pem')
        
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            raise FileNotFoundError(f"Certificate or key file not found. Cert: {cert_path}, Key: {key_path}")
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)
        print(f"SSL context created successfully with cert: {cert_path} and key: {key_path}")
        
        # Run HTTPS server in a separate thread
        https_thread = Thread(target=run_app, args=(context,))
        https_thread.start()
        print("HTTPS server started on port 5000")
        
        # Run HTTP server in the main thread
        print("Starting HTTP server on port 80")
        app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error creating SSL context: {str(e)}")
        print("Running without SSL due to configuration error")
        app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
