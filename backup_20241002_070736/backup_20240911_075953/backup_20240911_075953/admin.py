from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, User, Job, Application

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    # In a real application, you'd check if the user is an admin
    users = User.query.all()
    jobs = Job.query.all()
    applications = Application.query.all()
    return render_template('admin.html', users=users, jobs=jobs, applications=applications)

@admin_bp.route('/admin/add_job', methods=['POST'])
@login_required
def add_job():
    title = request.form.get('title')
    company = request.form.get('company')
    description = request.form.get('description')
    url = request.form.get('url')
    
    new_job = Job(title=title, company=company, description=description, url=url)
    db.session.add(new_job)
    db.session.commit()
    
    flash('New job added successfully')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        flash('Job deleted successfully')
    else:
        flash('Job not found')
    return redirect(url_for('admin.admin_dashboard'))
