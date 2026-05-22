"""
TEXT PREPROCESSING UTILITY - Multilingual (ID/EN), Multi-field
Mendukung lintas bahasa Indonesia-Inggris dan berbagai bidang
"""

import re

# ============================================================
# STOPWORDS (ID + EN)
# ============================================================
STOPWORDS = {
    # English
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
    'can', 'will', 'just', 'should', 'now', 'also', 'would', 'could',
    'may', 'might', 'must', 'shall', 'need', 'ought', 'used',
    # Indonesian
    'dan', 'atau', 'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan',
    'untuk', 'pada', 'adalah', 'dalam', 'tidak', 'ada', 'saya', 'kami',
    'kita', 'mereka', 'dia', 'akan', 'sudah', 'telah', 'sedang', 'bisa',
    'dapat', 'harus', 'juga', 'lebih', 'sangat', 'oleh', 'sebagai', 'serta',
    'karena', 'jika', 'bila', 'maka', 'namun', 'tetapi', 'namun', 'agar',
    'supaya', 'antara', 'selama', 'setelah', 'sebelum', 'tentang', 'terhadap',
    'bagi', 'kepada', 'bahwa', 'hal', 'cara', 'setiap', 'semua', 'para',
    'nya', 'pun', 'lah', 'kah', 'pula', 'yakni', 'yaitu', 'hingga', 'sampai'
}

# ============================================================
# CROSS-LANGUAGE SKILL MAPPING
# Kunci: semua sinonim/variasi → canonical English term
# ============================================================
SKILL_SYNONYMS = {
    # ── SOFT SKILLS ──────────────────────────────────────────
    'communication': [
        'komunikasi', 'komunikasi lisan', 'komunikasi tulisan',
        'verbal communication', 'written communication', 'public speaking',
        'presentasi', 'presentation', 'berbicara di depan umum'
    ],
    'teamwork': [
        'kerja tim', 'kerja sama tim', 'kerjasama tim', 'team work',
        'kolaborasi', 'collaboration', 'cooperative', 'bekerja sama',
        'team player', 'team collaboration'
    ],
    'leadership': [
        'kepemimpinan', 'memimpin', 'pemimpin', 'lead', 'leading',
        'team leader', 'ketua tim', 'manajerial', 'managerial'
    ],
    'problem solving': [
        'pemecahan masalah', 'memecahkan masalah', 'analytical thinking',
        'berpikir analitis', 'analytical', 'analitis', 'critical thinking',
        'berpikir kritis', 'troubleshooting', 'solusi masalah'
    ],
    'time management': [
        'manajemen waktu', 'mengatur waktu', 'punctual', 'tepat waktu',
        'deadline management', 'prioritization', 'prioritas'
    ],
    'adaptability': [
        'adaptasi', 'fleksibel', 'flexible', 'adaptif', 'mudah beradaptasi',
        'fast learner', 'cepat belajar', 'quick learner'
    ],
    'creativity': [
        'kreativitas', 'kreatif', 'creative thinking', 'inovatif', 'inovasi',
        'innovative', 'design thinking', 'out of the box'
    ],
    'attention to detail': [
        'teliti', 'ketelitian', 'detail oriented', 'detail-oriented',
        'cermat', 'accurate', 'akurat', 'presisi'
    ],
    'multitasking': [
        'multitasking', 'mengelola banyak tugas', 'mengerjakan banyak hal',
        'handle multiple tasks'
    ],
    'interpersonal skills': [
        'kemampuan interpersonal', 'relasi antar personal', 'hubungan antar manusia',
        'people skills', 'social skills', 'kemampuan sosial'
    ],

    # ── IT & PROGRAMMING ─────────────────────────────────────
    'python': ['python', 'py'],
    'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015'],
    'java': ['java', 'core java', 'java se', 'java ee'],
    'typescript': ['typescript', 'ts'],
    'php': ['php', 'php7', 'php8'],
    'sql': ['sql', 'query database', 'database query', 'structured query language'],
    'html': ['html', 'html5'],
    'css': ['css', 'css3', 'styling', 'stylesheet'],
    'react': ['react', 'reactjs', 'react.js'],
    'angular': ['angular', 'angularjs'],
    'vue': ['vue', 'vuejs', 'vue.js'],
    'django': ['django', 'django framework'],
    'flask': ['flask', 'flask framework'],
    'node.js': ['node', 'nodejs', 'node.js'],
    'machine learning': [
        'machine learning', 'ml', 'pembelajaran mesin', 'supervised learning',
        'unsupervised learning', 'model ml'
    ],
    'deep learning': ['deep learning', 'dl', 'neural network', 'jaringan saraf tiruan'],
    'data analysis': [
        'analisis data', 'data analytics', 'data analyst', 'analitik data',
        'pengolahan data', 'data processing'
    ],
    'data visualization': [
        'visualisasi data', 'data viz', 'dashboard', 'reporting', 'laporan visual'
    ],
    'git': ['git', 'version control', 'github', 'gitlab', 'bitbucket', 'kontrol versi'],
    'docker': ['docker', 'containerization', 'container'],
    'kubernetes': ['kubernetes', 'k8s', 'container orchestration'],
    'aws': ['aws', 'amazon web services', 'amazon cloud'],
    'azure': ['azure', 'microsoft azure', 'azure cloud'],
    'linux': ['linux', 'unix', 'ubuntu', 'centos', 'debian'],

    # ── MARKETING ────────────────────────────────────────────
    'digital marketing': [
        'pemasaran digital', 'digital marketing', 'online marketing',
        'pemasaran online', 'internet marketing', 'e-marketing'
    ],
    'social media marketing': [
        'media sosial', 'social media', 'sosmed', 'instagram marketing',
        'facebook ads', 'tiktok marketing', 'twitter marketing', 'konten media sosial'
    ],
    'seo': [
        'seo', 'search engine optimization', 'optimasi mesin pencari',
        'organic search', 'pencarian organik'
    ],
    'content marketing': [
        'content marketing', 'konten marketing', 'pemasaran konten',
        'content creation', 'pembuatan konten', 'copywriting', 'penulisan konten'
    ],
    'brand management': [
        'manajemen merek', 'brand management', 'branding', 'brand awareness',
        'kesadaran merek', 'brand identity'
    ],
    'market research': [
        'riset pasar', 'market research', 'penelitian pasar', 'analisis pasar',
        'market analysis', 'consumer insight', 'customer insight'
    ],
    'advertising': [
        'periklanan', 'iklan', 'advertising', 'ads', 'kampanye iklan',
        'ad campaign', 'google ads', 'paid ads', 'iklan berbayar'
    ],
    'email marketing': [
        'email marketing', 'newsletter', 'email campaign', 'kampanye email'
    ],
    'crm': [
        'crm', 'customer relationship management', 'manajemen hubungan pelanggan',
        'customer management', 'salesforce', 'hubspot'
    ],

    # ── FINANCE & ACCOUNTING ─────────────────────────────────
    'financial analysis': [
        'analisis keuangan', 'financial analysis', 'financial modeling',
        'pemodelan keuangan', 'financial reporting', 'laporan keuangan'
    ],
    'accounting': [
        'akuntansi', 'accounting', 'pembukuan', 'bookkeeping',
        'pencatatan keuangan', 'financial recording'
    ],
    'budgeting': [
        'penganggaran', 'budgeting', 'budget planning', 'perencanaan anggaran',
        'cost planning', 'perencanaan biaya'
    ],
    'tax': [
        'perpajakan', 'pajak', 'tax', 'taxation', 'brevet pajak',
        'tax planning', 'perencanaan pajak'
    ],
    'auditing': [
        'audit', 'auditing', 'pemeriksaan keuangan', 'internal audit',
        'audit internal', 'external audit'
    ],
    'microsoft excel': [
        'excel', 'microsoft excel', 'ms excel', 'spreadsheet', 'pivot table',
        'vlookup', 'formula excel'
    ],
    'financial statements': [
        'laporan keuangan', 'financial statements', 'neraca', 'balance sheet',
        'income statement', 'laporan laba rugi', 'cash flow', 'arus kas'
    ],
    'investment': [
        'investasi', 'investment', 'portfolio', 'portofolio', 'asset management',
        'manajemen aset'
    ],

    # ── HUMAN RESOURCES ──────────────────────────────────────
    'recruitment': [
        'rekrutmen', 'recruitment', 'hiring', 'seleksi karyawan',
        'talent acquisition', 'headhunting', 'sourcing kandidat'
    ],
    'training and development': [
        'pelatihan dan pengembangan', 'training development', 'td',
        'learning development', 'pengembangan sdm', 'pelatihan karyawan'
    ],
    'performance management': [
        'manajemen kinerja', 'performance management', 'kpi', 'penilaian kinerja',
        'performance review', 'performance appraisal'
    ],
    'compensation and benefits': [
        'kompensasi dan benefit', 'compensation benefits', 'payroll',
        'penggajian', 'remunerasi', 'remuneration', 'tunjangan'
    ],
    'labor law': [
        'hukum ketenagakerjaan', 'labor law', 'undang-undang tenaga kerja',
        'employment law', 'regulasi ketenagakerjaan', 'uu ketenagakerjaan'
    ],
    'employee relations': [
        'hubungan karyawan', 'employee relations', 'industrial relations',
        'hubungan industrial', 'ketenagakerjaan'
    ],
    'organizational development': [
        'pengembangan organisasi', 'organizational development', 'od',
        'manajemen perubahan', 'change management'
    ],

    # ── ENGINEERING ──────────────────────────────────────────
    'autocad': ['autocad', 'cad', 'computer aided design', 'desain berbantuan komputer'],
    'project management': [
        'manajemen proyek', 'project management', 'pengelolaan proyek',
        'pmp', 'prince2', 'scrum master', 'agile', 'waterfall'
    ],
    'quality control': [
        'kontrol kualitas', 'quality control', 'qc', 'quality assurance',
        'qa', 'pengendalian mutu', 'jaminan kualitas', 'iso'
    ],
    'lean manufacturing': [
        'lean manufacturing', 'lean', 'six sigma', 'kaizen', 'efisiensi produksi'
    ],
    'structural analysis': [
        'analisis struktur', 'structural analysis', 'structural engineering',
        'teknik struktur', 'desain struktur'
    ],
    'maintenance': [
        'pemeliharaan', 'maintenance', 'perawatan mesin', 'preventive maintenance',
        'corrective maintenance', 'pemeliharaan preventif'
    ],

    # ── EDUCATION / RESEARCH ─────────────────────────────────
    'research': [
        'penelitian', 'riset', 'research', 'kajian', 'studi',
        'literature review', 'tinjauan literatur'
    ],
    'teaching': [
        'mengajar', 'pengajaran', 'teaching', 'instruktur', 'instructor',
        'fasilitator', 'facilitator', 'trainer'
    ],
    'curriculum development': [
        'pengembangan kurikulum', 'curriculum development', 'desain pembelajaran',
        'instructional design', 'rancangan pembelajaran'
    ],
    'public speaking': [
        'public speaking', 'berbicara di depan umum', 'presentasi publik',
        'orasi', 'pidato', 'mc', 'master of ceremony'
    ],

    # ── DESIGN / CREATIVE ────────────────────────────────────
    'graphic design': [
        'desain grafis', 'graphic design', 'visual design', 'desain visual'
    ],
    'ui ux design': [
        'ui ux', 'ui/ux', 'user interface', 'user experience', 'desain antarmuka',
        'ux design', 'ui design', 'product design', 'figma', 'sketch', 'adobe xd'
    ],
    'photography': [
        'fotografi', 'photography', 'foto', 'kamera', 'editing foto', 'photo editing'
    ],
    'video editing': [
        'video editing', 'editing video', 'videografi', 'videography',
        'premiere pro', 'after effects', 'final cut', 'davinci resolve'
    ],
    'adobe photoshop': [
        'photoshop', 'adobe photoshop', 'ps', 'photo manipulation'
    ],
    'adobe illustrator': [
        'illustrator', 'adobe illustrator', 'ai', 'vector design', 'desain vektor'
    ],

    # ── CUSTOMER SERVICE / SALES ─────────────────────────────
    'customer service': [
        'layanan pelanggan', 'customer service', 'cs', 'pelayanan pelanggan',
        'customer support', 'customer care', 'after sales'
    ],
    'sales': [
        'penjualan', 'sales', 'selling', 'direct sales', 'b2b sales', 'b2c sales',
        'account management', 'business development', 'pengembangan bisnis'
    ],
    'negotiation': [
        'negosiasi', 'negotiation', 'bargaining', 'tawar menawar', 'deal closing'
    ],

    # ── LANGUAGES ────────────────────────────────────────────
    'english': [
        'bahasa inggris', 'english', 'inggris', 'toefl', 'ielts',
        'english proficiency', 'kemampuan bahasa inggris'
    ],
    'mandarin': [
        'bahasa mandarin', 'mandarin', 'chinese', 'bahasa china', 'hsk'
    ],
    'arabic': ['bahasa arab', 'arabic', 'arab'],
    'japanese': ['bahasa jepang', 'japanese', 'jepang', 'jlpt'],
}

# Build reverse lookup: setiap sinonim → canonical term
SYNONYM_TO_CANONICAL = {}
for canonical, synonyms in SKILL_SYNONYMS.items():
    SYNONYM_TO_CANONICAL[canonical.lower()] = canonical.lower()
    for syn in synonyms:
        SYNONYM_TO_CANONICAL[syn.lower()] = canonical.lower()

# All canonical skills (flat set for matching)
ALL_CANONICAL_SKILLS = set(SKILL_SYNONYMS.keys())


def normalize_skill(text_fragment):
    """Cek apakah text fragment cocok dengan sinonim manapun, return canonical"""
    text_lower = text_fragment.lower().strip()
    return SYNONYM_TO_CANONICAL.get(text_lower)


def extract_skills(text):
    """
    Extract skills dari teks, support lintas bahasa ID/EN.
    Return: set of canonical skill names
    """
    if not text:
        return set()

    text_lower = text.lower()
    found_skills = set()

    # Cek setiap sinonim dalam teks
    for synonym, canonical in SYNONYM_TO_CANONICAL.items():
        pattern = r'\b' + re.escape(synonym) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(canonical)

    return found_skills


def preprocess_text(text):
    """
    Preprocess teks: lowercase, hapus punctuation & angka, hapus stopwords.
    Tanpa NLTK — pure Python, aman untuk Vercel.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return ' '.join(tokens)


def preprocess_jd_and_resume(jd_text, resume_text):
    return preprocess_text(jd_text), preprocess_text(resume_text)