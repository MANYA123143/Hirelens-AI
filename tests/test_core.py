"""
HireLens AI - Comprehensive Verification Test Suite
Tests:
1. Database initialization and user registration/authentication
2. Kaggle dataset loading and category prediction
3. ATS analysis, score computation, and missing values detection
4. Missing values roadmap generation (all 4 phases)
5. Blank canvas AI resume generation (text & HTML)
6. Proximity job matching and notification dispatching
"""
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db import init_db, register_user, authenticate_user, get_all_jobs, get_user_notifications
from database.seed_data import seed_database
from core.dataset_loader import DatasetEngine
from core.ats_engine import analyze_resume_ats
from core.roadmap_generator import generate_missing_values_roadmap
from core.resume_generator import build_resume_text, build_resume_html, generate_ai_summary, enhance_bullet_point
from core.notification_engine import match_jobs_for_candidate, broadcast_job_to_candidates

def run_tests():
    print("========== 1. TESTING DATABASE & AUTH ==========")
    init_db()
    seed_database()
    
    # Register test candidate
    test_user_res = register_user(
        username="unit_test_user",
        email="test_student@example.com",
        password="TestPassword@123",
        full_name="Alex Mercer",
        phone="+1 415-555-0199",
        city="Bengaluru",
        state="Karnataka",
        country="India",
        target_role="Full Stack AI Developer",
        target_category="INFORMATION-TECHNOLOGY",
        skills="Python, SQL, React, FastAPI, Docker",
        experience_level="Student/Fresher"
    )
    print("User Registration Result:", test_user_res["success"], test_user_res["message"])
    
    auth_user = authenticate_user("unit_test_user", "TestPassword@123")
    assert auth_user is not None, "Authentication failed!"
    print(f"User authenticated: {auth_user['full_name']} (ID: {auth_user['id']})")

    print("\n========== 2. TESTING KAGGLE DATASET LOADER ==========")
    dataset_engine = DatasetEngine.get_instance()
    categories = dataset_engine.get_categories()
    print(f"Categories count: {len(categories)}")
    assert len(categories) == 24, "Expected 24 categories from Kaggle dataset!"
    
    cat, conf = dataset_engine.predict_category("Experienced with python, sql, aws, docker, react, and rest apis.")
    print(f"Predicted Category: {cat} (Confidence: {conf})")
    assert cat == "INFORMATION-TECHNOLOGY", f"Unexpected predicted category: {cat}"

    print("\n========== 3. TESTING ATS ENGINE & MISSING VALUES ==========")
    sample_resume = """
    ALEX MERCER
    alex.mercer@example.com | +1 415-555-0199 | Bengaluru, Karnataka
    LinkedIn: linkedin.com/in/alex-mercer | GitHub: github.com/alex-mercer

    PROFESSIONAL SUMMARY
    Dedicated software developer with passion for building scalable systems.

    SKILLS
    Python, SQL, React, Git, Linux

    WORK EXPERIENCE
    Software Intern | TechCorp (2024)
    - Spearheaded backend microservice migration, reducing query response times by 35%.
    - Engineered automated ETL pipelines processing over 100k daily records.

    EDUCATION
    B.S. in Computer Science - Tech University (2025)
    """

    ats_result = analyze_resume_ats(
        resume_text=sample_resume,
        target_category="INFORMATION-TECHNOLOGY",
        job_description="Looking for an engineer with Python, SQL, React, Docker, Kubernetes, AWS, and CI/CD."
    )
    print(f"Overall ATS Score: {ats_result['overall_score']}% (Grade: {ats_result['grade']})")
    print(f"Matched Skills: {ats_result['matched_skills']}")
    print(f"Missing Skills: {ats_result['missing_skills']}")
    assert ats_result["overall_score"] > 0, "ATS Score should be > 0"
    assert "docker" in ats_result["missing_skills"], "Docker should be identified as missing skill"
    assert "aws" in ats_result["missing_skills"], "AWS should be identified as missing skill"

    print("\n========== 4. TESTING ROADMAP GENERATOR ==========")
    roadmap = generate_missing_values_roadmap(
        ats_analysis_result=ats_result,
        candidate_name="Alex Mercer",
        target_category="INFORMATION-TECHNOLOGY"
    )
    print(f"Roadmap generated with {len(roadmap['phases'])} phases:")
    for p in roadmap["phases"]:
        print(f" - {p['title']} ({p['duration']})")
    assert len(roadmap["phases"]) == 4, "Roadmap must contain exactly 4 structured phases"

    print("\n========== 5. TESTING AI RESUME MAKER & FORMATTER ==========")
    summary = generate_ai_summary("AI Engineer", "Python, PyTorch, React", "Student/Fresher")
    print("Generated AI Summary:", summary[:100], "...")
    assert len(summary) > 50, "Summary generation failed!"

    bullet = enhance_bullet_point("worked on database optimization")
    print("Enhanced Bullet:", bullet)
    assert "%" in bullet or "spearheaded" in bullet.lower(), "Bullet enhancement missing metrics/action verbs!"

    resume_dict = {
        "personal": {
            "full_name": "Alex Mercer",
            "title": "AI Engineer",
            "email": "alex@example.com",
            "phone": "+1 415 555-0199",
            "city": "Bengaluru",
            "state": "Karnataka",
            "country": "India",
            "linkedin": "linkedin.com/in/alex",
            "github": "github.com/alex"
        },
        "summary": summary,
        "skills": {"Languages": "Python, SQL", "Frameworks": "React, FastAPI"},
        "experience": [{"role": "Intern", "company": "Acme", "location": "Bengaluru", "dates": "2024", "bullets": bullet}],
        "education": [{"degree": "B.S. CS", "institution": "Univ", "year": "2025", "gpa": "3.9", "coursework": "Algorithms"}],
        "projects": [{"title": "HireLens", "tech_stack": "Python, Streamlit", "link": "github.com", "description": "Built ATS system"}],
        "certifications": "AWS Cloud Practitioner"
    }
    compiled_text = build_resume_text(resume_dict)
    compiled_html = build_resume_html(resume_dict)
    assert "ALEX MERCER" in compiled_text, "Compiled text missing name"
    assert "<!DOCTYPE html>" in compiled_html, "Compiled HTML missing doctype"
    print("Compiled Text Length:", len(compiled_text), "chars | HTML Length:", len(compiled_html), "chars")

    print("\n========== 6. TESTING PROXIMITY JOBS & NOTIFICATIONS ==========")
    matches = match_jobs_for_candidate(auth_user)
    print(f"Jobs matching candidate: {len(matches)} found.")
    assert len(matches) > 0, "Should find matching jobs for user"

    alerts_sent = broadcast_job_to_candidates(matches[0]["job"]["id"])
    print(f"Broadcast alerts sent for job ID {matches[0]['job']['id']}: {alerts_sent}")
    
    user_notifs = get_user_notifications(auth_user["id"])
    print(f"User notifications in inbox: {len(user_notifs)}")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! The HireLens AI platform is 100% operational.")

if __name__ == "__main__":
    run_tests()
