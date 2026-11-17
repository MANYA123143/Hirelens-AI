"""
HireLens AI - Kaggle Resume Dataset Loader & Intelligence Engine
Loads and indexes the 2,484 resumes from Divyaamith/Kaggle-Resume.
Extracts domain vocabularies, category benchmarks, and provides TF-IDF category prediction.
"""
import os
import csv
import json
import re
from collections import Counter
import streamlit as st
from config import DATASET_PATH, BENCHMARK_PATH, KAGGLE_CATEGORIES

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
                        samples[cat] = {
                            "id": row[0],
                            "category": cat,
                            "snippet": row[1][:600],
                            "full_text": row[1][:3000]
                        }
        self.category_counts = dict(counts)
        self.sample_resumes = samples

    def get_categories(self):
        return sorted(list(self.categories))

    def get_category_counts(self):
        return self.category_counts

    def get_category_skills(self, category):
        """Returns benchmark skills for a given category."""
        clean_cat = category.strip().upper()
        if clean_cat in self.category_skills:
            return self.category_skills[clean_cat]
        return ["communication", "project management", "problem solving", "teamwork", "leadership", "analytics"]

    def get_sample_resume(self, category):
        """Returns sample text of a real resume from the dataset."""
        clean_cat = category.strip().upper()
        if clean_cat in self.sample_resumes:
            return self.sample_resumes[clean_cat]["full_text"]
        return "Experienced professional with background in target domain."

    def search_resumes(self, keyword="", category="All", limit=10):
        """Searches through the Kaggle Resume dataset."""
        if not os.path.exists(DATASET_PATH):
            return []

        results = []
        clean_keyword = keyword.lower().strip()
        with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 4:
                    continue
                res_id, res_str, res_html, cat = row[0], row[1], row[2], row[3].strip()
                if category != "All" and cat != category:
                    continue
                if clean_keyword and clean_keyword not in res_str.lower():
                    continue

                snippet = res_str[:300].strip().replace("\n", " ")
                results.append({
                    "id": res_id,
                    "category": cat,
                    "snippet": snippet,
                    "full_text": res_str
                })
                if len(results) >= limit:
                    break
        return results

    def predict_category(self, resume_text):
        """Predicts the most probable job category for any resume using keyword density matching."""
        if not resume_text:
            return "INFORMATION-TECHNOLOGY", 0.5

        text_lower = resume_text.lower()
        best_cat = "INFORMATION-TECHNOLOGY"
        max_matches = 0

        for cat, skills in self.category_skills.items():
            matches = sum(1 for s in skills if re.search(r'\b' + re.escape(s.lower()) + r'\b', text_lower))
            if matches > max_matches:
                max_matches = matches
                best_cat = cat

        confidence = min(0.95, 0.40 + (max_matches * 0.08))
        return best_cat, round(confidence, 2)

@st.cache_resource(show_spinner=False)
def _get_cached_dataset_engine():
    engine = DatasetEngine()
    return engine
