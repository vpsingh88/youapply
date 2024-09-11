from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Job, Application
from openai_chat_completion.chat_request import send_openai_request
import json

job_matching_bp = Blueprint('job_matching', __name__)

@job_matching_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@job_matching_bp.route('/get_job_suggestions')
@login_required
def get_job_suggestions():
    # This is a simplified version. In a real-world scenario, you'd implement a more sophisticated matching algorithm.
    user_preferences = current_user.job_preferences
    matching_jobs = Job.query.filter(
        Job.title.ilike(f"%{user_preferences['job_type']}%")
    ).limit(3).all()
    
    suggestions = []
    for job in matching_jobs:
        # Use OpenAI to customize job description based on user's CV
        prompt = f"Customize this job description for the user's CV:\nJob: {job.title}\nDescription: {job.description}\nUser CV: {current_user.cv_data}"
        customized_description = send_openai_request(prompt)
        
        suggestions.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'description': customized_description,
            'url': job.url
        })
    
    return jsonify(suggestions)

@job_matching_bp.route('/apply_job', methods=['POST'])
@login_required
def apply_job():
    job_id = request.form.get('job_id')
    job = Job.query.get(job_id)
    if job:
        application = Application(user_id=current_user.id, job_id=job.id)
        db.session.add(application)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Application submitted successfully'})
    return jsonify({'success': False, 'message': 'Job not found'})

@job_matching_bp.route('/track_applications')
@login_required
def track_applications():
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('track_applications.html', applications=applications)
