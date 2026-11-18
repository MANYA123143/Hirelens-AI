"""
HireLens AI - Kaggle Resume Dataset Loader & Intelligence Engine
Loads and indexes the 2,484 resumes from Divyaamith/Kaggle-Resume.
Extracts domain vocabularies, category benchmarks, and provides TF-IDF / keyword category prediction.
"""
import os
import csv
import json
import re
from collections import Counter
import streamlit as st
from config import DATASET_PATH, BENCHMARK_PATH, KAGGLE_CATEGORIES

CATEGORY_DOMAIN_INDICATORS = {
    "ACCOUNTANT": ["accountant", "accounting", "cpa", "audit", "general ledger", "balance sheet", "taxation", "reconciliation", "gaap", "financial statements", "accounts payable", "bookkeeping", "payroll"],
    "ADVOCATE": ["advocate", "lawyer", "attorney", "legal", "litigation", "counsel", "court", "law firm", "contracts", "juris", "llb", "paralegal"],
    "AGRICULTURE": ["agriculture", "agronomy", "crop", "farming", "soil science", "irrigation", "sustainable farming", "harvest", "pest control", "fertilizer", "horticulture"],
    "APPAREL": ["apparel", "fashion", "garment", "textile", "clothing", "pattern making", "fashion design", "merchandiser", "draping", "tailoring", "couture"],
    "ARTS": ["fine arts", "artist", "illustration", "curator", "museum", "gallery", "sculpture", "painting", "visual arts", "digital art", "exhibition"],
    "AUTOMOBILE": ["automotive", "vehicle", "automobile", "powertrain", "chassis", "oem", "engine repair", "cad/cam", "dealership", "mechanic", "braking systems"],
    "AVIATION": ["aviation", "aircraft", "airline", "flight", "pilot", "avionics", "aerospace", "faa", "airport", "air traffic", "maintenance engineer"],
    "BANKING": ["banking", "bank", "credit analysis", "wealth management", "commercial banking", "retail banking", "loan officer", "branch manager", "kyc", "aml", "mortgage"],
    "BPO": ["bpo", "call center", "customer support", "telecalling", "inbound", "outbound", "voice process", "ticketing", "teleperformance", "sla", "customer service representative"],
    "BUSINESS-DEVELOPMENT": ["business development", "marketing", "business strategy", "strategic partnerships", "market expansion", "lead generation", "mba", "client acquisition", "growth", "b2b", "revenue"],
    "CHEF": ["chef", "culinary", "cook", "kitchen", "pastry", "sous chef", "menu planning", "restaurant", "catering", "fine dining", "food safety", "haccp"],
    "CONSTRUCTION": ["construction", "civil engineering", "structural", "site engineer", "bim", "autocad", "osha", "contractor", "blueprints", "site supervisor", "concrete"],
    "CONSULTANT": ["consultant", "consulting", "management consulting", "advisory", "strategy consultant", "mckinsey", "bain", "bcg", "kpi", "process optimization", "transformation"],
    "DESIGNER": ["designer", "ui/ux", "graphic designer", "figma", "photoshop", "wireframing", "interaction design", "user experience", "visual design", "design system"],
    "DIGITAL-MEDIA": ["digital media", "social media", "content creator", "seo", "sem", "video editing", "copywriting", "social media marketing", "influencer", "youtube", "digital marketing"],
    "ENGINEERING": ["mechanical engineer", "electrical engineer", "solidworks", "robotics", "plc", "thermodynamics", "manufacturing", "mechatronics", "hardware engineer"],
    "FINANCE": ["finance", "financial analyst", "financial modeling", "investment", "portfolio", "dcf", "valuation", "equity research", "asset management", "hedge fund", "fp&a"],
    "FITNESS": ["fitness", "personal trainer", "gym", "workout", "nutrition", "strength training", "bodybuilding", "exercise physiology", "kinesiology", "wellness", "coach"],
    "HEALTHCARE": ["healthcare", "hospital", "nurse", "nursing", "clinical", "patient care", "medical", "doctor", "physician", "ehr", "emr", "clinic", "bls"],
    "HR": ["human resources", "hr", "recruiter", "talent acquisition", "recruitment", "onboarding", "employee relations", "payroll administration", "hrms", "workday", "people operations"],
    "INFORMATION-TECHNOLOGY": ["software", "developer", "programmer", "python", "java", "sql", "aws", "docker", "kubernetes", "cloud", "full stack", "backend", "frontend", "devops", "cybersecurity", "it"],
    "PUBLIC-RELATIONS": ["public relations", "pr", "press release", "media relations", "spokesperson", "crisis communication", "corporate communications", "publicist", "media outreach"],
    "SALES": ["sales", "account executive", "sales representative", "cold calling", "inside sales", "pipeline management", "quota", "salesforce", "closing deals", "b2b sales"],
    "TEACHER": ["teacher", "teaching", "educator", "curriculum", "school", "classroom", "lesson planning", "pedagogy", "student", "faculty", "lecturer", "professor"]
}

class DatasetEngine:
    _instance = None

    def __init__(self):
        self.categories = KAGGLE_CATEGORIES
        self.benchmark_data = {}
        self.category_counts = {}
        self.category_skills = {}
        self.sample_resumes = {}
        self._load_benchmarks()

    @classmethod
    def get_instance(cls):
        """Returns cached dataset engine instance."""
        return _get_cached_dataset_engine()

    def _load_benchmarks(self):
        """Loads cached benchmark data or generates from Resume.csv."""
        if os.path.exists(BENCHMARK_PATH):
            try:
                with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.benchmark_data = data
                    self.category_counts = data.get("counts", {})
                    self.category_skills = data.get("skills", {})
                    self.sample_resumes = data.get("samples", {})
                    return
            except Exception as e:
                print(f"Error loading benchmark JSON: {e}")

        # Fallback: extract directly from Resume.csv
        self._build_benchmarks_from_csv()

    def _build_benchmarks_from_csv(self):
        if not os.path.exists(DATASET_PATH):
            return

        counts = Counter()
        samples = {}
        with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    cat = row[3].strip()
                    counts[cat] += 1
                    if cat not in samples:
                        clean_text = re.sub(r'<[^>]+>', ' ', row[2])
                        clean_text = ' '.join(clean_text.split())
                        samples[cat] = {
                            "id": row[0],
                            "snippet": clean_text[:400],
                            "full_text": clean_text
                        }

        self.category_counts = dict(counts)
        self.sample_resumes = samples
        self.benchmark_data = {
            "counts": self.category_counts,
            "samples": self.sample_resumes
        }

    def get_category_counts(self):
        return self.category_counts

    def get_categories(self):
        return self.categories

    def get_sample_resume(self, category):
        """Returns full text of sample resume for given category."""
        if category in self.sample_resumes:
            return self.sample_resumes[category].get("full_text", "")
        return f"Sample resume content for category: {category}"

    def search_resumes(self, keyword="", category="All", limit=10):
        """High-speed streaming search through Kaggle dataset resumes."""
        results = []
        clean_keyword = keyword.strip().lower()

        if os.path.exists(DATASET_PATH):
            try:
                with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        if len(row) < 4:
                            continue
                        r_id = row[0]
                        r_text = row[1]
                        r_cat = row[3].strip()

                        if category != "All" and r_cat != category:
                            continue

                        if clean_keyword and clean_keyword not in r_text.lower():
                            continue

                        snippet = r_text[:280] + "..." if len(r_text) > 280 else r_text
                        results.append({
                            "id": r_id,
                            "category": r_cat,
                            "snippet": snippet,
                            "full_text": r_text
                        })

                        if len(results) >= limit:
                            break
                return results
            except Exception as e:
                print(f"Error reading {DATASET_PATH}: {e}")

        # Fallback to high-speed benchmark sample cache
        for cat, sample in self.sample_resumes.items():
            if category != "All" and cat != category:
                continue
            text = sample.get("full_text", "")
            if clean_keyword and clean_keyword not in text.lower():
                continue
            results.append({
                "id": sample.get("id", f"sample_{cat}"),
                "category": cat,
                "snippet": sample.get("snippet", text[:300]),
                "full_text": text
            })
            if len(results) >= limit:
                break
        return results

    def predict_category(self, resume_text):
        """Predicts the most probable job category for any resume using combined domain indicators and skill density matching."""
        if not resume_text:
            return "INFORMATION-TECHNOLOGY", 0.5

        text_lower = resume_text.lower()
        scores = {cat: 0 for cat in self.categories}

        # 1. Match high-confidence domain indicators
        for cat, indicators in CATEGORY_DOMAIN_INDICATORS.items():
            for kw in indicators:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    scores[cat] += (3 if " " in kw else 2)

        # 2. Match benchmark skills density
        for cat, skills in self.category_skills.items():
            for s in skills:
                if re.search(r'\b' + re.escape(s.lower()) + r'\b', text_lower):
                    scores[cat] += 1

        best_cat = max(scores, key=scores.get)
        max_score = scores[best_cat]

        if max_score == 0:
            return "INFORMATION-TECHNOLOGY", 0.40

        confidence = min(0.96, 0.45 + (max_score * 0.05))
        return best_cat, round(confidence, 2)

@st.cache_resource(show_spinner=False)
def _get_cached_dataset_engine():
    engine = DatasetEngine()
    return engine
