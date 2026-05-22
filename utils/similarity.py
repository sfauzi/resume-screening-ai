"""
SIMILARITY CALCULATION UTILITY
TF-IDF Cosine Similarity + Cross-language skill gap analysis
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(job_description, resume_text):
    """
    Hitung similarity score antara JD dan resume (0-100).
    """
    if not job_description or not resume_text:
        return 0.0

    try:
        tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=1000
        )
        tfidf_matrix = tfidf_vectorizer.fit_transform([job_description, resume_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return round(float(similarity[0][0]) * 100, 2)
    except Exception:
        return 0.0


def get_matching_skills(jd_skills, resume_skills):
    """
    Return (matching_skills, missing_skills) berdasarkan canonical skill names.
    Otomatis handle lintas bahasa karena extract_skills sudah normalisasi ke canonical.
    """
    matching = jd_skills.intersection(resume_skills)
    missing = jd_skills.difference(resume_skills)
    return matching, missing


def get_skill_score(jd_skills, resume_skills):
    """Hitung skill match score (0-100)"""
    if not jd_skills:
        return 100.0
    matching = jd_skills.intersection(resume_skills)
    return round(len(matching) / len(jd_skills) * 100, 1)


def get_combined_score(similarity_score, skill_score):
    """Gabungkan TF-IDF score (40%) dan skill score (60%)"""
    return round(similarity_score * 0.4 + skill_score * 0.6, 2)


def get_recommendations(jd_skills, resume_skills, similarity_score, skill_score):
    """
    Generate rekomendasi lengkap:
    - Overall assessment
    - Missing skills dengan saran konkret
    - Cross-language note jika ada gap bahasa
    """
    matching, missing = get_matching_skills(jd_skills, resume_skills)
    combined = get_combined_score(similarity_score, skill_score)

    recommendations = []

    # ── Overall Assessment ────────────────────────────────────
    if combined >= 80:
        overall = "🟢 Excellent Match! Profil kamu sangat sesuai dengan posisi ini."
    elif combined >= 60:
        overall = "🟡 Good Match. Profil kamu cukup sesuai, dengan beberapa area yang bisa ditingkatkan."
    elif combined >= 40:
        overall = "🟠 Moderate Match. Ada beberapa gap yang perlu diperhatikan sebelum melamar."
    else:
        overall = "🔴 Low Match. Profil kamu perlu pengembangan lebih lanjut untuk posisi ini."

    recommendations.append(overall)

    # ── Missing Skills Recommendations ───────────────────────
    if missing:
        missing_list = list(missing)

        # Kategorikan missing skills
        soft_missing = [s for s in missing_list if s in {
            'communication', 'teamwork', 'leadership', 'problem solving',
            'time management', 'adaptability', 'creativity', 'interpersonal skills',
            'attention to detail', 'multitasking', 'negotiation', 'public speaking'
        }]
        tech_missing = [s for s in missing_list if s not in soft_missing]

        if tech_missing:
            shown = tech_missing[:5]
            recommendations.append(
                f"💻 Skill teknis yang perlu ditambahkan ke CV: {', '.join(shown)}"
                + (f" (+{len(tech_missing)-5} lainnya)" if len(tech_missing) > 5 else "")
            )

        if soft_missing:
            shown = soft_missing[:3]
            recommendations.append(
                f"🤝 Soft skill yang disebutkan di JD tapi belum terlihat di CV: {', '.join(shown)}"
            )

        # Tip penulisan CV lintas bahasa
        recommendations.append(
            "🌐 Tips: Pastikan CV kamu mencantumkan skill dalam bahasa yang sama "
            "dengan job description (atau keduanya), karena sistem ATS sering "
            "mencocokkan kata kunci secara harfiah."
        )
    else:
        recommendations.append("✨ Semua skill yang diminta sudah tercantum di CV kamu!")

    # ── Specific Score-based Tips ─────────────────────────────
    if similarity_score < 40:
        recommendations.append(
            "📝 Skor kemiripan teks rendah — coba gunakan kata-kata yang sama "
            "seperti yang ada di job description dalam CV kamu."
        )
    if skill_score >= 80 and similarity_score < 50:
        recommendations.append(
            "ℹ️ Skill kamu sudah cocok, tapi gunakan terminologi yang lebih mirip "
            "dengan JD agar lolos filter ATS."
        )

    return recommendations


def detect_language_gaps(jd_skills, resume_skills, jd_text, resume_text):
    """
    Deteksi kemungkinan gap akibat perbedaan bahasa.
    Contoh: JD pakai 'communication', CV pakai 'komunikasi' → sudah dihitung sama.
    Return: daftar canonical skill yang kemungkinan ada di resume tapi beda bahasa.
    """
    from utils.preprocessing import SYNONYM_TO_CANONICAL

    missing, _ = resume_skills.difference(jd_skills), None
    gaps = []

    # Ini untuk UI info saja — actual matching sudah handle via canonical
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    for canonical, synonyms_list in __import__('utils.preprocessing',
                                               fromlist=['SKILL_SYNONYMS']).SKILL_SYNONYMS.items():
        # Skill ada di JD (dalam bahasa apapun)
        jd_has = any(re.search(r'\b' + re.escape(s) + r'\b', jd_lower)
                     for s in synonyms_list + [canonical])
        # Skill ada di resume (dalam bahasa apapun)
        resume_has = any(re.search(r'\b' + re.escape(s) + r'\b', resume_lower)
                         for s in synonyms_list + [canonical])

        if jd_has and resume_has and canonical in jd_skills and canonical in resume_skills:
            # Cek apakah kata yang dipakai berbeda bahasa
            jd_word = next((s for s in synonyms_list + [canonical]
                            if re.search(r'\b' + re.escape(s) + r'\b', jd_lower)), None)
            resume_word = next((s for s in synonyms_list + [canonical]
                                if re.search(r'\b' + re.escape(s) + r'\b', resume_lower)), None)
            if jd_word and resume_word and jd_word != resume_word:
                gaps.append({'jd_term': jd_word, 'resume_term': resume_word, 'canonical': canonical})

    return gaps[:8]  # max 8 untuk UI