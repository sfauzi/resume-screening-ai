"""
RESUME SCREENING AI - MAIN APPLICATION
Flask web application untuk screening CV dengan AI
"""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf
from utils.preprocessing import preprocess_text, extract_skills
from utils.similarity import calculate_similarity, get_matching_skills, get_recommendations

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # For flashing messages

# Configuration
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page - upload form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze resume against job description
    """
    # Check if both file and job description are provided
    if 'resume' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    if 'job_description' not in request.form:
        flash('Job description is required', 'error')
        return redirect(url_for('index'))
    
    file = request.files['resume']
    job_description = request.form['job_description']
    
    # Check if filename is empty
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check file type
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return redirect(url_for('index'))
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        flash('File size must be less than 5MB', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Step 1: Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)
        
        if not resume_text:
            flash('Could not extract text from PDF. Please ensure the file is not corrupted.', 'error')
            # Clean up
            os.remove(filepath)
            return redirect(url_for('index'))
        
        # Step 2: Preprocess texts
        processed_jd = preprocess_text(job_description)
        processed_resume = preprocess_text(resume_text)
        
        # Step 3: Extract skills
        jd_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)
        
        # Step 4: Calculate similarity score
        similarity_score = calculate_similarity(processed_jd, processed_resume)
        
        # Step 5: Get matching and missing skills
        matching_skills, missing_skills = get_matching_skills(jd_skills, resume_skills)
        
        # Step 6: Get recommendations
        recommendation = get_recommendations(missing_skills, similarity_score)
        
        # Prepare result data
        result = {
            'score': similarity_score,
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'recommendation': recommendation,
            'jd_word_count': len(processed_jd.split()),
            'resume_word_count': len(processed_resume.split())
        }
        
        # Clean up - delete uploaded file
        os.remove(filepath)
        
        return render_template('result.html', result=result)
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        flash(f'An error occurred during analysis: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 5MB', 'error')
    return redirect(url_for('index'))

@app.route('/test')
def test():
    errors = []
    
    try:
        from utils.pdf_parser import extract_text_from_pdf
    except Exception as e:
        errors.append(f"pdf_parser: {str(e)}")
    
    try:
        from utils.preprocessing import preprocess_text, extract_skills
    except Exception as e:
        errors.append(f"preprocessing: {str(e)}")
    
    try:
        from utils.similarity import calculate_similarity
    except Exception as e:
        errors.append(f"similarity: {str(e)}")

    if errors:
        return "<br>".join(errors), 500
    return "All imports OK!", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)