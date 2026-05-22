"""
TEXT PREPROCESSING UTILITY
Fungsi: Membersihkan dan memproses teks untuk NLP
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (hanya sekali)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Daftar skill umum untuk programming/web development
COMMON_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 
    'kotlin', 'go', 'rust', 'typescript', 'html', 'css', 'sql',
    
    # Frameworks & Libraries
    'flask', 'django', 'react', 'angular', 'vue', 'node.js', 'express',
    'spring', 'laravel', 'rails', 'bootstrap', 'jquery', 'pandas', 'numpy',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'firebase', 'redis', 'oracle',
    
    # Tools & Technologies
    'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins',
    'jira', 'linux', 'agile', 'scrum', 'rest api', 'graphql',
    
    # Data Science & AI
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'nlp', 'computer vision', 'data analysis', 'data visualization',
    
    # Soft Skills
    'teamwork', 'leadership', 'communication', 'problem solving',
    'critical thinking', 'project management', 'time management'
}

def preprocess_text(text):
    """
    Preprocess text untuk NLP analysis
    
    Steps:
    1. Lowercase
    2. Remove punctuation
    3. Remove numbers
    4. Remove stopwords
    5. Tokenization
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove punctuation dan special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 3. Remove numbers
    text = re.sub(r'\d+', ' ', text)
    
    # 4. Remove extra whitespace
    text = ' '.join(text.split())
    
    # 5. Tokenization
    tokens = word_tokenize(text)
    
    # 6. Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # 7. Remove short words (length < 3)
    tokens = [token for token in tokens if len(token) > 2]
    
    return ' '.join(tokens)

def extract_skills(text):
    """
    Extract skills from text based on common skills list
    
    Args:
        text (str): Input text
        
    Returns:
        set: Set of skills found in text
    """
    if not text:
        return set()
    
    # Lowercase the text
    text = text.lower()
    
    found_skills = set()
    
    # Check for each skill in the text
    for skill in COMMON_SKILLS:
        # Use word boundary to match whole words
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    
    return found_skills

def preprocess_jd_and_resume(jd_text, resume_text):
    """
    Preprocess both job description and resume text
    
    Args:
        jd_text (str): Job description text
        resume_text (str): Resume text
        
    Returns:
        tuple: (processed_jd, processed_resume)
    """
    processed_jd = preprocess_text(jd_text)
    processed_resume = preprocess_text(resume_text)
    
    return processed_jd, processed_resume