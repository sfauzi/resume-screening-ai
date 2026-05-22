"""
SIMILARITY CALCULATION UTILITY
Fungsi: Menghitung kemiripan antara JD dan CV menggunakan TF-IDF & Cosine Similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(job_description, resume_text):
    """
    Calculate similarity score between job description and resume
    
    Args:
        job_description (str): Processed job description text
        resume_text (str): Processed resume text
        
    Returns:
        float: Similarity score (0-100)
    """
    if not job_description or not resume_text:
        return 0.0
    
    # Create list of documents
    documents = [job_description, resume_text]
    
    # Create TF-IDF Vectorizer
    # ngram_range=(1,2) untuk menangkap bigrams juga
    tfidf_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words='english',
        max_features=1000
    )
    
    # Fit and transform documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity between first document (JD) and second (resume)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    # Convert to percentage
    similarity_score = similarity[0][0] * 100
    
    return round(similarity_score, 2)

def get_matching_skills(jd_skills, resume_skills):
    """
    Get matching and missing skills between JD and resume
    
    Args:
        jd_skills (set): Skills from job description
        resume_skills (set): Skills from resume
        
    Returns:
        tuple: (matching_skills, missing_skills)
    """
    matching_skills = jd_skills.intersection(resume_skills)
    missing_skills = jd_skills.difference(resume_skills)
    
    return matching_skills, missing_skills

def get_recommendations(missing_skills, similarity_score):
    """
    Generate recommendations based on missing skills and score
    
    Args:
        missing_skills (set): Skills not found in resume
        similarity_score (float): Overall similarity score
        
    Returns:
        str: Recommendation text
    """
    if similarity_score >= 80:
        if missing_skills:
            return "Excellent match! Just a few skills to add for perfection."
        else:
            return "Perfect match! You're an ideal candidate for this position."
    elif similarity_score >= 60:
        if missing_skills:
            return f"Good match! Consider adding these skills: {', '.join(list(missing_skills)[:3])}..."
        else:
            return "Good match! Your profile aligns well with the requirements."
    elif similarity_score >= 40:
        return f"Moderate match. Focus on developing: {', '.join(list(missing_skills)[:5])}..."
    else:
        return "Low match. Consider gaining more experience in the required areas."