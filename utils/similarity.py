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


def get_radar_data(jd_skills, resume_skills):
    """
    Hitung skor per kategori skill untuk radar chart.
    Return: list of dict {category, jd_count, resume_count, score, matching, missing}
    """
    SKILL_CATEGORIES = {
        'Soft Skills': {
            'communication', 'teamwork', 'leadership', 'problem solving',
            'time management', 'adaptability', 'creativity', 'attention to detail',
            'multitasking', 'interpersonal skills', 'negotiation', 'public speaking'
        },
        'IT & Dev': {
            'python', 'javascript', 'java', 'typescript', 'php', 'sql', 'html',
            'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js',
            'machine learning', 'deep learning', 'data analysis', 'data visualization',
            'git', 'docker', 'kubernetes', 'aws', 'azure', 'linux'
        },
        'Marketing': {
            'digital marketing', 'social media marketing', 'seo', 'content marketing',
            'brand management', 'market research', 'advertising', 'email marketing', 'crm'
        },
        'Finance': {
            'financial analysis', 'accounting', 'budgeting', 'tax', 'auditing',
            'microsoft excel', 'financial statements', 'investment'
        },
        'HR & Org': {
            'recruitment', 'training and development', 'performance management',
            'compensation and benefits', 'labor law', 'employee relations',
            'organizational development'
        },
        'Design': {
            'graphic design', 'ui ux design', 'photography', 'video editing',
            'adobe photoshop', 'adobe illustrator'
        },
        'Engineering': {
            'autocad', 'project management', 'quality control',
            'lean manufacturing', 'structural analysis', 'maintenance'
        },
        'Sales & Service': {
            'customer service', 'sales', 'negotiation'
        },
    }

    radar = []
    for category, skills_in_cat in SKILL_CATEGORIES.items():
        jd_in_cat = jd_skills.intersection(skills_in_cat)
        resume_in_cat = resume_skills.intersection(skills_in_cat)

        # Hanya tampilkan kategori yang relevan
        if not jd_in_cat and not resume_in_cat:
            continue

        jd_count = len(jd_in_cat)
        resume_count = len(resume_in_cat)

        if jd_count > 0:
            score = round(len(jd_in_cat.intersection(resume_in_cat)) / jd_count * 100)
        elif resume_count > 0:
            score = 100
        else:
            score = 0

        radar.append({
            'category': category,
            'jd_count': jd_count,
            'resume_count': resume_count,
            'score': score,
            'matching': sorted(list(jd_in_cat.intersection(resume_in_cat))),
            'missing': sorted(list(jd_in_cat.difference(resume_in_cat))),
        })

    radar.sort(key=lambda x: x['jd_count'], reverse=True)
    return radar


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

def get_keyword_highlight_data(resume_text, jd_skills):
    """
    Kembalikan teks CV dengan anotasi keyword:
    - found: keyword JD yang ditemukan di CV
    - missing: keyword JD yang TIDAK ditemukan di CV
    
    Return: list of dict {word, type} — type: 'found' | 'missing' | 'normal'
    Untuk keperluan rendering highlight di template.
    """
    import re

    if not resume_text or not jd_skills:
        return []

    # Buat peta: canonical skill → set of surface forms (untuk matching)
    from utils.preprocessing import SKILL_SYNONYMS

    # Flatten: semua surface form → canonical
    surface_to_canonical = {}
    for canonical, synonyms_list in SKILL_SYNONYMS.items():
        for s in synonyms_list + [canonical]:
            surface_to_canonical[s.lower()] = canonical

    resume_lower = resume_text.lower()

    # Deteksi semua surface form yang ada di resume (multi-word dulu)
    found_spans = {}  # (start, end) → type

    all_surfaces = sorted(surface_to_canonical.keys(), key=len, reverse=True)
    for surface in all_surfaces:
        canonical = surface_to_canonical[surface]
        if canonical not in jd_skills:
            continue
        pattern = r'\b' + re.escape(surface) + r'\b'
        for m in re.finditer(pattern, resume_lower):
            # Cek overlap
            overlap = any(
                not (m.end() <= s or m.start() >= e)
                for (s, e) in found_spans
            )
            if not overlap:
                hit_type = 'found' if canonical in jd_skills else 'missing'
                # Skill ada di JD, sekarang cek apakah ada di resume_skills
                found_spans[(m.start(), m.end())] = hit_type

    # Tandai missing: skill JD yang surface form-nya TIDAK ditemukan di resume
    jd_found_canonicals = {
        surface_to_canonical[sf]
        for (start, end), _ in found_spans.items()
        for sf in [resume_lower[start:end]]
        if sf in surface_to_canonical
    }
    missing_jd = jd_skills - jd_found_canonicals

    # Rekonstruksi teks sebagai token list
    # Potong resume menjadi max 3000 karakter agar tidak terlalu panjang di UI
    display_text = resume_text[:3000] + ('...' if len(resume_text) > 3000 else '')
    display_lower = display_text.lower()

    # Re-scan pada display_text
    highlight_spans = {}  # start → (end, type, original_text)

    for surface in all_surfaces:
        canonical = surface_to_canonical[surface]
        if canonical not in jd_skills:
            continue
        is_found = canonical in jd_found_canonicals or True  # re-evaluate below
        # Cek apakah canonical ada di resume (found) atau tidak (missing)
        # Kita pakai: jika surface ditemukan di display_lower → found, else skip
        pattern = r'\b' + re.escape(surface) + r'\b'
        for m in re.finditer(pattern, display_lower):
            overlap = any(
                not (m.end() <= s or m.start() >= e)
                for s in highlight_spans
                for e in [highlight_spans[s][0]]
            )
            if not overlap:
                highlight_spans[m.start()] = (m.end(), 'found', display_text[m.start():m.end()])

    # Bangun token list
    tokens = []
    pos = 0
    for start in sorted(highlight_spans.keys()):
        end, tok_type, original = highlight_spans[start]
        if start > pos:
            tokens.append({'text': display_text[pos:start], 'type': 'normal'})
        tokens.append({'text': original, 'type': tok_type})
        pos = end
    if pos < len(display_text):
        tokens.append({'text': display_text[pos:], 'type': 'normal'})

    # Tambahkan missing skill sebagai info (bukan span teks, tapi badge info)
    missing_info = sorted(list(missing_jd))

    return {
        'tokens': tokens,
        'missing_keywords': missing_info,
        'found_count': len(highlight_spans),
        'missing_count': len(missing_jd),
    }    