# 🎯 HireLens AI - Next-Gen Resume Intelligence & Career Ecosystem

> Built 100% in **Pure Python** powered by the **Hugging Face Kaggle-Resume Dataset** ([Divyaamith/Kaggle-Resume](https://huggingface.co/datasets/Divyaamith/Kaggle-Resume)).

---

## 🌟 Key Features

### 1. 🔐 User Authentication & Personal Details Management
- **Login & Sign-Up System**: Secure password hashing with salt (SHA-256) stored in a local SQLite database (`hirelens.db`).
- **Personal Details Collection**: Gathers full name, email, phone number, **City, State, and Country**, target job title, target industry domain, and key skills.
- **Smart Notification Engine**: Personal details and skills feed the real-time matching engine that triggers instant alert pop-ups when matching jobs arise.

### 2. 🎯 AI Resume Analysis & ATS Checker
- **Multi-Format Input**: Upload `.pdf` resumes (parsed using `pypdf`), `.txt` files, paste resume text, or load benchmark sample resumes directly from the Kaggle dataset.
- **Multi-Factor ATS Scoring (0 - 100%)**:
  - **Keywords & Skill Match (35%)**: Evaluates overlap against job descriptions and domain taxonomies.
  - **Section Completeness (25%)**: Audits 6 critical ATS sections (Contact, Summary, Experience, Education, Skills, Projects).
  - **Action Verbs & Impact Metrics (20%)**: Identifies strong action verbs and quantifiable results (`%`, `$`, scale).
  - **Readability & Formatting (20%)**: Audits length, word count, contact accessibility, and ATS parser safety.
- **Actionable Gap Analysis**: Visualizes matched skills (green), missing critical skills (red), and section checks.

### 3. 📈 Step-by-Step Roadmap for Missing Values & Skills
- Tailored **4-Phase Learning & Career Roadmap** generated dynamically based on the exact gaps detected:
  - **Phase 1: Immediate Resume Optimization & Gap Elimination** (1–3 Days): Fixes missing contact info, missing sections, and weak bullet points.
  - **Phase 2: Core Missing Skills Mastery** (2–3 Weeks): Curated documentation, free courses, and hands-on milestones for each missing skill.
  - **Phase 3: Proof-of-Skill Portfolio Projects** (2–3 Weeks): High-impact project concepts with architectural deliverables and ready-to-use resume bullet points.
  - **Phase 4: ATS Validation, Certification & Job Applications** (Week 6): Industry certifications, ATS re-testing, and local job applications.
- **Interactive Progress Tracker**: Check off completed tasks with a live milestone completion bar.

### 4. 📝 AI Resume Maker (Blank Canvas for Students)
- Clean, structured form designed for students and job seekers to fill in from scratch:
  - Personal & Contact Information
  - Professional Summary with **✨ AI Polish / Generate Summary**
  - Categorized Skills & Tools
  - Work & Internship Experience with **✨ AI Bullet Enhancer**
  - Key Academic / Personal Projects
  - Education History & Coursework
  - Certifications & Honors
- **Live ATS-Compliant Preview**: Styled in modern Harvard/Tech single-column format with zero table traps.
- **Export Options**: Download Printable HTML (prints to PDF via `Ctrl+P`) or Plain Text.
- **One-Click ATS Transfer**: Send the newly constructed resume straight to the ATS Checker with one button.

### 5. 🗺️ Nearby Job Opportunities & Interactive World Map
- **Interactive 3D World Map (Pydeck & Plotly)**: Pinpoints job opportunities worldwide with interactive markers, color-coded by match score and category.
- **Proximity Filtering**: Automatically prioritizes jobs nearby in the candidate's registered **City and State** or remote openings.
- **Multi-Dimensional Filters**: Filter by Category (24 Kaggle domains), Job Type (Full-time, Remote, Hybrid, On-site), and Keyword/Skill search.
- **Recruiter Tool**: Post new job requirements with real-time broadcasting to matching candidates!

### 6. 🔔 Real-Time Notification Pop-up Alerts
- Candidates receive prominent **notification pop-up alert banners** on their dashboard and in their Notification Center whenever new positions matching their skills and city/state are detected.
- Includes a test alert simulation trigger.

### 7. 📊 Hugging Face Kaggle-Resume Dataset Explorer
- Explores all 2,484 resumes across 24 industry categories from `Divyaamith/Kaggle-Resume`.
- Visualizes category distributions, benchmark skill taxonomies, and provides a full-text resume search with one-click ATS benchmarking.

---

## 🚀 How to Run the Application

The entire project is written in **100% Python**. Run the following command from this directory:

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
`http://localhost:8501`

---

## 📂 Project Structure

```
Hirelens AI Python/
│
├── Resume.csv                        # Kaggle Resume dataset (2,484 resumes, 24 categories)
├── benchmark_resumes.json            # Fast-indexed category skills & benchmark samples
├── hirelens.db                       # SQLite database (Users, Jobs, Notifications, Resumes)
├── app.py                            # Streamlit entry point
├── config.py                         # App constants, categories, theme styling
│
├── database/
│   ├── __init__.py
│   ├── db.py                         # SQLite ORM & authentication functions
│   └── seed_data.py                  # Global jobs seeder with city coordinates
│
├── core/
│   ├── __init__.py
│   ├── dataset_loader.py             # Kaggle dataset parser & TF-IDF category predictor
│   ├── ats_engine.py                 # Multi-factor ATS Scorer & missing values detector
│   ├── roadmap_generator.py          # Dynamic 4-phase learning & career roadmap engine
│   ├── resume_generator.py           # AI resume builder, bullet polisher, HTML export
│   └── notification_engine.py        # Location & skill matching engine, alert trigger
│
├── pages_modules/
│   ├── __init__.py
│   ├── login_page.py                 # Login / Registration with personal details & location
│   ├── dashboard_page.py             # User home dashboard & real-time notification banner
│   ├── ats_analyzer_page.py          # ATS Score Checker & sections audit
│   ├── roadmap_page.py               # Missing values & skills dynamic career roadmap
│   ├── resume_maker_page.py          # Blank canvas AI Resume Maker for students
│   ├── job_opportunities_page.py     # Interactive World Map + City/State proximity jobs
│   ├── profile_page.py               # Candidate personal details, alert settings & history
│   └── dataset_explorer_page.py      # Hugging Face Kaggle-Resume dataset viewer & analytics
│
├── assets/
│   └── style.css                     # Premium modern UI styling
│
└── tests/
    └── test_core.py                  # Automated test suite
```
