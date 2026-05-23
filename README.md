# Resume Screening AI

Aplikasi screening CV berbasis AI yang menganalisis kecocokan resume dengan job description menggunakan NLP (Natural Language Processing). Mendukung multi-bahasa (Indonesia & English) dan berbagai bidang pekerjaan.

## Fitur Utama

- **Overall Match Score**: Skor kecocokan gabungan dari text similarity (TF-IDF) dan skill match
- **Skill Radar**: Visualisasi coverage skill per kategori (IT, Marketing, Finance, HR, Engineering, dll)
- **Cross-language Support**: Deteksi dan translasi otomatis antara Bahasa Indonesia dan English
- **Multi-bidang**: Bekerja untuk berbagai industri (bukan hanya programming)
- **Smart Recommendations**: Rekomendasi AI berdasarkan gap skill dan bahasa
- **Keyword Highlighter**: Menyorot kata kunci yang cocok antara CV dan JD
- **Analysis Statistics**: Statistik lengkap (word count, skill match ratio, dll)

## Tech Stack

- Flask 2.3.3
- PyPDF2 3.0.1 (PDF text extraction)
- scikit-learn 1.4.0 (TF-IDF & Cosine Similarity)
- NLTK 3.8.1 (Text preprocessing)
- deep-translator 1.11.4 (Multi-language translation)
- TailwindCSS (UI styling)

## Prasyarat

- Python 3.12 atau lebih baru
- pip (Python package manager)
- Virtual environment (direkomendasikan)

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/sfauzi/resume-screening-ai.git
cd resume-screening-ai
```

### 2. Buat Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# atau

venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

```

### 4. Jalankan Aplikasi
```bash
python3 app.py

```
Buka browser di:
```bash
http://localhost:5000

```
## Cara Penggunaan

1. Upload CV (format PDF)
2. Paste atau tulis Job Description
3. Klik **"Analyze CV Now"**
4. Lihat hasil analisis:
   - Match score (persentase)
   - Skill yang cocok dan tidak ditemukan
   - Rekomendasi AI
   - Statistik analisis

---

## Skor Analisis

Overall match score dihitung dengan formula:

- **Text Similarity (TF-IDF)**: 40% bobot
- **Skill Match (ID+EN)**: 60% bobot

Skill match dihitung berdasarkan database skill yang mencakup:

- Soft Skills (komunikasi, teamwork, leadership, dll)
- Hard Skills (sesuai bidang masing-masing)
- Technical Skills (IT, engineering)
- Business Skills (marketing, finance, HR)

---

## Multi-language Support

Sistem mendeteksi bahasa CV dan Job Description secara otomatis:

- Bahasa Indonesia
- English

Jika bahasa berbeda, sistem akan melakukan translasi otomatis ke English menggunakan `deep-translator` untuk analisis yang akurat.

### Demo

Akses demo live di: 
#### https://resume-screening-ai-mu.vercel.app

