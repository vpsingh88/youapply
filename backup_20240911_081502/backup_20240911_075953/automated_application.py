from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import db, Job, Application
from openai_chat_completion.chat_request import send_openai_request

automated_application_bp = Blueprint('automated_application', __name__)

@automated_application_bp.route('/auto_apply', methods=['POST'])
@login_required
def auto_apply():
    job_id = request.form.get('job_id')
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'})
    
    # Customize CV and cover letter using OpenAI
    cv_prompt = f"Customize this CV for the job:\nJob: {job.title}\nDescription: {job.description}\nOriginal CV: {current_user.cv_data}"
    customized_cv = send_openai_request(cv_prompt)
    
    cover_letter_prompt = f"Write a cover letter for this job:\nJob: {job.title}\nDescription: {job.description}\nCV: {customized_cv}"
    cover_letter = send_openai_request(cover_letter_prompt)
    
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to job application page
        driver.get(job.url)
        
        # Fill in application form (this is a simplified example)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(current_user.name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(current_user.email)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cv"))).send_keys(customized_cv)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cover_letter"))).send_keys(cover_letter)
        
        # Submit application
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit"))).click()
        
        # Record application in database
        application = Application(user_id=current_user.id, job_id=job.id)
        db.session.add(application)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Application submitted successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error during application: {str(e)}'})
    
    finally:
        driver.quit()
