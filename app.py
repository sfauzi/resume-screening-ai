"""
RESUME SCREENING AI - MAIN APPLICATION
Flask web application untuk screening CV dengan AI (Multilingual ID/EN)
"""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf
from utils.preprocessing import preprocess_text, extract_skills
from utils.similarity import (
    calculate_similarity, get_matching_skills,
    get_skill_score, get_combined_score, get_recommendations,
    detect_language_gaps, get_radar_data
)

app = Flask(__name__)
app.secret_key = 'resume-screening-ai-secret-2024'

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    file = request.files['resume']
    job_description = request.form.get('job_description', '').strip()

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return redirect(url_for('index'))

    if not job_description:
        flash('Job description is required', 'error')
        return redirect(url_for('index'))

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        flash('File size must be less than 5MB', 'error')
        return redirect(url_for('index'))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Step 1: Extract PDF
        resume_text = extract_text_from_pdf(filepath)
        os.remove(filepath)

        if not resume_text or len(resume_text.strip()) < 30:
            flash('Could not extract text from PDF. Make sure it is not a scanned image.', 'error')
            return redirect(url_for('index'))

        # Step 2: Preprocess (untuk TF-IDF)
        processed_jd = preprocess_text(job_description)
        processed_resume = preprocess_text(resume_text)

        # Step 3: Extract skills (lintas bahasa, canonical)
        jd_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)

        # Step 4: Scores
        similarity_score = calculate_similarity(processed_jd, processed_resume)
        skill_score = get_skill_score(jd_skills, resume_skills)
        combined_score = get_combined_score(similarity_score, skill_score)

        # Step 5: Matching / missing
        matching_skills, missing_skills = get_matching_skills(jd_skills, resume_skills)

        # Step 6: Recommendations
        recommendations = get_recommendations(
            jd_skills, resume_skills, similarity_score, skill_score
        )

        # Step 7: Detect cross-language pairs
        language_gaps = detect_language_gaps(jd_skills, resume_skills, job_description, resume_text)

        # Step 8: Radar chart data per kategori
        radar_data = get_radar_data(jd_skills, resume_skills)

        result = {
            'combined_score': combined_score,
            'similarity_score': similarity_score,
            'skill_score': skill_score,
            'matching_skills': sorted(list(matching_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'recommendations': recommendations,
            'language_gaps': language_gaps,
            'radar_data': radar_data,
            'jd_word_count': len(processed_jd.split()),
            'resume_word_count': len(processed_resume.split()),
            'jd_skills_count': len(jd_skills),
            'resume_skills_count': len(resume_skills),
        }

        return render_template('result.html', result=result)

    except Exception as e:
        print(f"Error: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 5MB', 'error')
    return redirect(url_for('index'))


@app.route('/test')
def test():
    errors = []
    try:
        from utils.pdf_parser import extract_text_from_pdf
    except Exception as e:
        errors.append(f"pdf_parser: {e}")
    try:
        from utils.preprocessing import preprocess_text, extract_skills
        # Test cross-language
        jd = extract_skills("We need communication skills and teamwork")
        cv = extract_skills("Saya memiliki kemampuan komunikasi dan kerja tim yang baik")
        match = jd.intersection(cv)
        errors.append(f"Cross-lang test — JD: {jd}, CV: {cv}, Match: {match}")
    except Exception as e:
        errors.append(f"preprocessing: {e}")
    try:
        from utils.similarity import calculate_similarity
    except Exception as e:
        errors.append(f"similarity: {e}")

    return "<br>".join(errors) if errors else "All OK!", 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)