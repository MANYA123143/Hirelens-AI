"""
HireLens AI - Configuration and Application Constants
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hirelens.db")
DATASET_PATH = os.path.join(BASE_DIR, "Resume.csv")
BENCHMARK_PATH = os.path.join(BASE_DIR, "benchmark_resumes.json")

# 24 Job Categories directly derived from the Kaggle Resume Dataset (Divyaamith/Kaggle-Resume)
KAGGLE_CATEGORIES = [
    "ACCOUNTANT",
    "ADVOCATE",
    "AGRICULTURE",
    "APPAREL",
    "ARTS",
    "AUTOMOBILE",
    "AVIATION",
    "BANKING",
    "BPO",
    "BUSINESS-DEVELOPMENT",
    "CHEF",
    "CONSTRUCTION",
    "CONSULTANT",
    "DESIGNER",
    "DIGITAL-MEDIA",
    "ENGINEERING",
    "FINANCE",
    "FITNESS",
    "HEALTHCARE",
    "HR",
    "INFORMATION-TECHNOLOGY",
    "PUBLIC-RELATIONS",
    "SALES",
    "TEACHER"
]

# Action verbs that boost ATS scores
ATS_ACTION_VERBS = [
    "achieved", "acquired", "adapted", "administered", "analyzed", "automated",
    "built", "budgeted", "calculated", "collaborated", "composed", "conducted",
    "constructed", "coordinated", "created", "decreased", "delivered", "deployed",
    "designed", "developed", "devised", "directed", "documented", "drove",
    "engineered", "enhanced", "established", "evaluated", "executed", "expanded",
    "expedited", "fabricated", "formulated", "founded", "generated", "guided",
    "implemented", "improved", "increased", "initiated", "innovated", "inspected",
    "instituted", "integrated", "launched", "lead", "led", "managed", "maximized",
    "mentored", "migrated", "minimized", "modeled", "modernized", "negotiated",
    "optimized", "orchestrated", "organized", "overhauled", "oversaw", "partnered",
    "performed", "pioneered", "planned", "produced", "programmed", "published",
    "reduced", "refactored", "resolved", "restructured", "revamped", "scaled",
    "scheduled", "secured", "simplified", "spearheaded", "standardized", "streamlined",
    "strengthened", "structured", "supervised", "synthesized", "trained", "transformed",
    "troubleshot", "unified", "upgraded", "validated", "visualized"
]

# Essential Resume Sections for ATS evaluation
ATS_ESSENTIAL_SECTIONS = [
    "Contact Information",
    "Professional Summary",
    "Work Experience",
    "Education",
    "Skills",
    "Projects"
]

# App Theme Colors
PRIMARY_COLOR = "#2563EB"    # Modern Royal Blue
SECONDARY_COLOR = "#0D9488"  # Teal
ACCENT_COLOR = "#7C3AED"     # Purple
BG_DARK = "#0F172A"
CARD_BG = "#1E293B"
TEXT_LIGHT = "#F8FAFC"
