"""
TEXT PREPROCESSING UTILITY - No NLTK (Vercel compatible)
"""

import re

# Stopwords manual — tidak perlu NLTK download
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm',
    'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn',
    'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan',
    'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'also', 'would', 'could',
    'may', 'might', 'must', 'shall', 'need', 'dare', 'ought', 'used'
}

COMMON_SKILLS = {
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
    'kotlin', 'go', 'rust', 'typescript', 'html', 'css', 'sql',
    'flask', 'django', 'react', 'angular', 'vue', 'node.js', 'express',
    'spring', 'laravel', 'rails', 'bootstrap', 'jquery', 'pandas', 'numpy',
    'mysql', 'postgresql', 'mongodb', 'firebase', 'redis', 'oracle',
    'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins',
    'jira', 'linux', 'agile', 'scrum', 'rest api', 'graphql',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'nlp', 'computer vision', 'data analysis', 'data visualization',
    'teamwork', 'leadership', 'communication', 'problem solving',
    'critical thinking', 'project management', 'time management'
}

def preprocess_text(text):
    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Hapus punctuation
    text = re.sub(r'[^\w\s]', ' ', text)

    # 3. Hapus angka
    text = re.sub(r'\d+', ' ', text)

    # 4. Tokenize pakai split biasa — tidak perlu NLTK
    tokens = text.split()

    # 5. Hapus stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]

    # 6. Hapus kata pendek
    tokens = [t for t in tokens if len(t) > 2]

    return ' '.join(tokens)

def extract_skills(text):
    if not text:
        return set()
    text = text.lower()
    found_skills = set()
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    return found_skills

def preprocess_jd_and_resume(jd_text, resume_text):
    return preprocess_text(jd_text), preprocess_text(resume_text)