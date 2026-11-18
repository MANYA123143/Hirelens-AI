"""
HireLens AI - Comprehensive ATS Score & Resume Analysis Engine
Evaluates Technical, Soft, Leadership, Analytical, and Domain Skills.
Computes multi-factor ATS score, section completeness, action verbs, metrics, and detects missing values.
"""
import re
import io
import pypdf
from config import ATS_ACTION_VERBS, ATS_ESSENTIAL_SECTIONS

try:
    from core.dataset_loader import DatasetEngine
    from core.skills_taxonomy import ALL_SKILLS_LIST, SKILL_CATEGORIES, classify_skill, get_skills_for_category
except ModuleNotFoundError:
    from dataset_loader import DatasetEngine
    from skills_taxonomy import ALL_SKILLS_LIST, SKILL_CATEGORIES, classify_skill, get_skills_for_category

COMMON_SKILLS_TAXONOMY = ALL_SKILLS_LIST

def extract_text_from_pdf(pdf_file_bytes) -> str:
    """Extracts raw text content from uploaded PDF bytes using pypdf."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_file_bytes))
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_skills_from_text(text: str) -> list[str]:
    """Extracts all recognized technical and non-technical skills using optimized pattern matching with punctuation stripping and lemmatization."""
    if not text:
        return []
    text_lower = f" {text.lower()} "
    
    # 1. Clean token extraction for O(1) single-word lookups
    # Strips punctuation so words followed by periods, commas, parentheses (e.g. "Python.", "SQL,") are cleanly captured
    raw_tokens = re.findall(r'[a-z0-9#+.-]+', text_lower)
    words_set = set()
    for t in raw_tokens:
        clean = t.strip('.,;:!?()[]{}"\'`/*')
        if clean:
            words_set.add(clean)
            # Lemmatized plural / suffix variants
            if clean.endswith('s') and len(clean) > 3 and not clean.endswith('ss'):
                words_set.add(clean[:-1])
            if clean.endswith('ies') and len(clean) > 4:
                words_set.add(clean[:-3] + 'y')

    found = []
    for skill in ALL_SKILLS_LIST:
        if " " in skill or "." in skill or "-" in skill or "/" in skill:
            # Multi-word or special-character phrase: word-boundary match
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        else:
            if skill in words_set:
                found.append(skill)

    return sorted(list(set(found)))

def detect_sections(text: str) -> dict[str, bool]:
    """Detects essential resume sections based on typical header patterns."""
    text_lower = text.lower()
    sections = {
        "Contact Information": bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text) or re.search(r'(\+?\d[\d -]{8,15}\d)', text)),
        "Professional Summary": bool(re.search(r'\b(summary|objective|profile|about me|professional summary)\b', text_lower)),
        "Work Experience": bool(re.search(r'\b(experience|employment|work history|professional experience|internship|career history)\b', text_lower)),
        "Education": bool(re.search(r'\b(education|academic|degree|university|college|b\.tech|bachelor|master|phd|diploma)\b', text_lower)),
        "Skills": bool(re.search(r'\b(skills|technical skills|soft skills|competencies|technologies|proficiencies|expertise)\b', text_lower)),
        "Projects": bool(re.search(r'\b(projects|key projects|academic projects|personal projects|portfolio)\b', text_lower))
    }
    return sections

def detect_action_verbs(text: str) -> list[str]:
    """Finds power action verbs in the resume."""
    text_lower = text.lower()
    found_verbs = []
    for verb in ATS_ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, text_lower):
            found_verbs.append(verb)
    return sorted(list(set(found_verbs)))

def detect_quantifiable_metrics(text: str) -> list[str]:
    """Extracts bullet points or fragments containing percentages, metrics, or dollar figures."""
    patterns = [
        r'\b\d+%\b',
        r'\$\s*\d+(?:,\d+)*(?:\.\d+)?(?:k|m|b)?',
        r'\b\d+(?:\.\d+)?\s*(?:x|times|users|clients|customers|increase|decrease|growth|boost|reduction|saved|scale)\b',
        r'\b(?:reduced|improved|increased|boosted|accelerated|cut|saved)\s+[^.]+?\b\d+%'
    ]
    matches = []
    for p in patterns:
        for m in re.finditer(p, text, re.IGNORECASE):
            start = max(0, m.start() - 25)
            end = min(len(text), m.end() + 25)
            snippet = text[start:end].strip().replace("\n", " ")
            if snippet not in matches:
                matches.append(snippet)
    return matches[:8]

def categorize_skills_list(skills: list[str]) -> dict[str, list[str]]:
    """Groups a list of skills into Technical, Soft, Leadership, Analytical, and Business categories."""
    grouped = {
        "Technical & Software": [],
        "Soft & Interpersonal": [],
        "Leadership & Management": [],
        "Analytical & Problem Solving": [],
        "Business & Domain": []
    }
    for sk in skills:
        cat = classify_skill(sk)
        if cat in grouped:
            grouped[cat].append(sk)
        elif cat in ["HR, People & Operations", "Finance, Accounting & Banking", "Healthcare & Medical", "Design & Creative", "Education & Instruction", "Legal, Compliance & Policy", "Hospitality, Fitness & Culinary", "Business, Sales & Marketing"]:
            grouped["Business & Domain"].append(sk)
        else:
            grouped["Technical & Software"].append(sk)
    return {k: v for k, v in grouped.items() if v}

def analyze_resume_ats(resume_text: str, target_category: str = "INFORMATION-TECHNOLOGY", job_description: str = "") -> dict:
    """
    Comprehensive ATS Analysis Engine.
    Evaluates both technical and non-technical skills, section completeness, action verbs, metrics, and detects gaps.
    """
    dataset_engine = DatasetEngine.get_instance()
    text = resume_text.strip()
    word_count = len(text.split())

    # Predict probable category from Kaggle model
    predicted_cat, predicted_conf = dataset_engine.predict_category(text)

    # 1. Target Skills Identification (Technical + Non-Technical)
    target_skills = []
    if job_description and len(job_description.strip()) > 30:
        target_skills = extract_skills_from_text(job_description)
    
    if not target_skills:
        category_benchmark_skills = get_skills_for_category(target_category)
        target_skills = [s.lower() for s in category_benchmark_skills]

    # 2. Extract Candidate Skills (All recognized skills in resume)
    candidate_skills = extract_skills_from_text(text)
    
    # 3. Match Skills Calculation against Target
    matched_skills = [s for s in target_skills if s in candidate_skills]
    missing_skills = [s for s in target_skills if s not in candidate_skills]
    
    # Categorize matched, missing, and full candidate skills
    matched_by_cat = categorize_skills_list(matched_skills)
    missing_by_cat = categorize_skills_list(missing_skills)
    candidate_by_cat = categorize_skills_list(candidate_skills)

    tech_matched = len(matched_by_cat.get("Technical & Software", []))
    tech_missing = len(missing_by_cat.get("Technical & Software", []))
    tech_total = tech_matched + tech_missing
    tech_match_pct = round((tech_matched / tech_total * 100.0), 1) if tech_total > 0 else (100.0 if not tech_missing else 0.0)

    soft_matched = sum(len(v) for k, v in matched_by_cat.items() if k != "Technical & Software")
    soft_missing = sum(len(v) for k, v in missing_by_cat.items() if k != "Technical & Software")
    soft_total = soft_matched + soft_missing
    soft_match_pct = round((soft_matched / soft_total * 100.0), 1) if soft_total > 0 else (100.0 if not soft_missing else 0.0)

    skill_match_pct = (len(matched_skills) / len(target_skills) * 100) if target_skills else 70.0
    skill_match_score = min(100.0, round(skill_match_pct, 1))

    # 4. Section Completeness Check
    sections = detect_sections(text)
    detected_sections_count = sum(1 for v in sections.values() if v)
    section_score = round((detected_sections_count / len(sections)) * 100.0, 1)

    # 5. Action Verbs & Metrics
    found_verbs = detect_action_verbs(text)
    metrics_found = detect_quantifiable_metrics(text)
    
    verb_score = min(100.0, len(found_verbs) * 10.0)
    metric_score = min(100.0, len(metrics_found) * 20.0)
    impact_score = round((verb_score * 0.5) + (metric_score * 0.5), 1)

    # 6. Readability & Formatting
    readability_score = 100.0
    formatting_issues = []

    if word_count < 250:
        readability_score -= 30.0
        formatting_issues.append("Resume is too short (< 250 words). Provide more detailed achievements.")
    elif word_count > 1200:
        readability_score -= 20.0
        formatting_issues.append("Resume is overly long (> 1200 words). Aim for a concise 1-2 page structure.")

    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
    has_phone = bool(re.search(r'(\+?\d[\d -]{8,15}\d)', text))
    has_links = bool(re.search(r'(linkedin\.com|github\.com|portfolio|http)', text, re.IGNORECASE))

    if not has_email:
        readability_score -= 15.0
        formatting_issues.append("Missing professional contact email address.")
    if not has_phone:
        readability_score -= 10.0
        formatting_issues.append("Missing phone number for recruiter outreach.")
    if not has_links:
        readability_score -= 10.0
        formatting_issues.append("No LinkedIn or GitHub/Portfolio link detected.")

    readability_score = max(10.0, round(readability_score, 1))

    # 7. Weighted Total ATS Score
    # Weights: Skill Match (35%), Section Completeness (25%), Impact/Metrics (20%), Readability/Format (20%)
    overall_score = round(
        (skill_match_score * 0.35) +
        (section_score * 0.25) +
        (impact_score * 0.20) +
        (readability_score * 0.20),
        1
    )
    overall_score = min(100.0, max(0.0, overall_score))

    # 8. Grade Assignment
    if overall_score >= 85:
        grade = "A"
        grade_label = "ATS Ready (Excellent)"
        badge_color = "#10B981"
    elif overall_score >= 70:
        grade = "B"
        grade_label = "Competitive (Good)"
        badge_color = "#3B82F6"
    elif overall_score >= 55:
        grade = "C"
        grade_label = "Needs Optimization"
        badge_color = "#F59E0B"
    else:
        grade = "D"
        grade_label = "Critical Gaps Detected"
        badge_color = "#EF4444"

    # 9. Missing Values and Gaps Identification
    missing_values = {
        "missing_skills": missing_skills,
        "missing_technical_skills": missing_by_cat.get("Technical & Software", []),
        "missing_soft_skills": [sk for cat, skl in missing_by_cat.items() if cat != "Technical & Software" for sk in skl],
        "missing_sections": [sec for sec, exists in sections.items() if not exists],
        "lacks_quantifiable_metrics": len(metrics_found) < 3,
        "lacks_action_verbs": len(found_verbs) < 5,
        "formatting_issues": formatting_issues,
        "missing_contact_info": {
            "email": not has_email,
            "phone": not has_phone,
            "links": not has_links
        }
    }

    # 10. High-Impact Recommendations
    recommendations = []
    if missing_by_cat.get("Technical & Software"):
        top_tech = ", ".join(missing_by_cat["Technical & Software"][:4])
        recommendations.append(f"Add technical expertise and project proof for: **{top_tech}**.")
    
    missing_soft_list = missing_values["missing_soft_skills"]
    if missing_soft_list:
        top_soft = ", ".join(missing_soft_list[:4])
        recommendations.append(f"Demonstrate non-technical & soft skills with examples: **{top_soft}**.")

    if missing_values["missing_sections"]:
        sec_list = ", ".join(missing_values["missing_sections"])
        recommendations.append(f"Include dedicated sections for: **{sec_list}**.")
    if missing_values["lacks_quantifiable_metrics"]:
        recommendations.append("Quantify your achievements using numbers (e.g., 'Improved response time by 35%', 'Managed $50k budget').")
    if missing_values["lacks_action_verbs"]:
        recommendations.append("Begin bullet points with strong power action verbs (e.g., 'Spearheaded', 'Engineered', 'Optimized', 'Negotiated').")
    if not has_links:
        recommendations.append("Add your LinkedIn profile URL and GitHub or online portfolio link at the top.")

    return {
        "overall_score": overall_score,
        "grade": grade,
        "grade_label": grade_label,
        "badge_color": badge_color,
        "word_count": word_count,
        "sub_scores": {
            "skill_match": skill_match_score,
            "technical_match": tech_match_pct,
            "soft_match": soft_match_pct,
            "section_completeness": section_score,
            "impact_metrics": impact_score,
            "readability_formatting": readability_score
        },
        "target_category": target_category,
        "predicted_category": predicted_cat,
        "predicted_confidence": predicted_conf,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_by_category": matched_by_cat,
        "missing_by_category": missing_by_cat,
        "candidate_by_category": candidate_by_cat,
        "candidate_skills": candidate_skills,
        "target_skills": target_skills,
        "sections_audit": sections,
        "found_verbs": found_verbs,
        "metrics_found": metrics_found,
        "missing_values": missing_values,
        "recommendations": recommendations
    }
