"""
HireLens AI - Missing Values & Skills Career Roadmap Generator
Constructs a personalized 4-phase learning and portfolio roadmap to bridge identified resume gaps.
"""

# Resource and project guides mapped to commonly missing skills
SKILL_LEARNING_GUIDES = {
    "python": {
        "title": "Python for Software Engineering & Data",
        "resources": ["Official Python Docs (docs.python.org)", "freeCodeCamp Python Masterclass", "Automate the Boring Stuff"],
        "project": "Build an asynchronous REST API or automated data processing script with logging and unit tests."
    },
    "docker": {
        "title": "Containerization with Docker",
        "resources": ["Docker Getting Started Guide (docs.docker.com)", "Docker for Beginners (freeCodeCamp)", "Play with Docker Labs"],
        "project": "Dockerize a multi-service web application with Docker Compose, including a database and caching layer."
    },
    "aws": {
        "title": "AWS Cloud Foundations",
        "resources": ["AWS Skill Builder (Free Tier)", "freeCodeCamp AWS Cloud Practitioner Masterclass"],
        "project": "Deploy a serverless application using AWS Lambda, S3, API Gateway, and CloudFront."
    },
    "kubernetes": {
        "title": "Container Orchestration with Kubernetes",
        "resources": ["Kubernetes.io Tutorials", "Nana's Kubernetes 101 Course", "Minikube Local Lab"],
        "project": "Deploy a microservice cluster using Minikube with Helm charts, ingress controller, and auto-scaling."
    },
    "react": {
        "title": "Modern Frontend Development with React",
        "resources": ["React.dev Official Docs", "Scrimba React Course", "FullStackOpen (University of Helsinki)"],
        "project": "Develop a responsive dashboard with state management, API data fetching, and dark mode toggles."
    },
    "sql": {
        "title": "Relational Databases & Advanced SQL",
        "resources": ["Mode Analytics SQL Tutorial", "SQLZoo Interactive Exercises", "LeetCode SQL 50"],
        "project": "Design a normalized e-commerce database schema, write complex window functions and indexing strategies."
    },
    "machine learning": {
        "title": "Applied Machine Learning & Scikit-Learn",
        "resources": ["StatQuest with Josh Starmer", "Andrew Ng's Machine Learning Specialization", "Scikit-learn Documentation"],
        "project": "Build an end-to-end churn prediction pipeline with hyperparameter tuning and model explainability (SHAP)."
    },
    "fastapi": {
        "title": "High-Performance APIs with FastAPI",
        "resources": ["FastAPI Official Docs (tiangolo.com)", "TestDriven.io FastAPI Tutorials"],
        "project": "Create a high-speed CRUD microservice with JWT authentication, Pydantic validation, and OpenAPI documentation."
    },
    "git": {
        "title": "Professional Version Control & CI/CD",
        "resources": ["Pro Git Book (git-scm.com)", "GitHub Skills Interactive Labs"],
        "project": "Configure automated GitHub Actions workflows with linting, unit testing, and automated release tags."
    },
    "figma": {
        "title": "UI/UX Design Systems in Figma",
        "resources": ["Figma Academy", "Refactoring UI by Adam Wathan", "Google UX Design Professional Certificate"],
        "project": "Create a comprehensive design system featuring modular components, auto-layout, and interactive prototypes."
    },
    "seo": {
        "title": "Technical & Content SEO Mastery",
        "resources": ["Moz Beginner's Guide to SEO", "Google Search Central Documentation", "Ahrefs Academy"],
        "project": "Perform a complete technical SEO audit on an e-commerce website and create an optimized content cluster."
    },
    "financial modeling": {
        "title": "Corporate Financial Modeling & Valuation",
        "resources": ["Corporate Finance Institute (CFI) Free Resources", "Aswath Damodaran Valuation Lectures"],
        "project": "Build a 3-statement financial model and DCF valuation for a publicly listed technology company."
    },
    "recruitment": {
        "title": "Modern Talent Acquisition & Sourcing",
        "resources": ["LinkedIn Talent Solutions Guides", "SHRM Talent Acquisition Resources"],
        "project": "Design a complete end-to-end recruitment funnel, candidate scoring rubrics, and ATS onboarding workflow."
    }
}

def generate_missing_values_roadmap(ats_analysis_result: dict, candidate_name: str = "Candidate", target_category: str = "Target Domain") -> dict:
    """
    Constructs a detailed 4-phase step-by-step roadmap to eliminate missing values,
    acquire missing skills, and maximize ATS score.
    """
    missing_vals = ats_analysis_result.get("missing_values", {})
    missing_skills = ats_analysis_result.get("missing_skills", [])
    missing_sections = missing_vals.get("missing_sections", [])
    formatting_issues = missing_vals.get("formatting_issues", [])
    contact_gaps = missing_vals.get("missing_contact_info", {})

    phases = []

    # ==================== PHASE 1: IMMEDIATE RESUME FIXES (Days 1 - 3) ====================
    phase1_tasks = []
    
    if contact_gaps.get("email"):
        phase1_tasks.append({
            "task": "Add a professional email address (e.g., firstname.lastname@gmail.com) in the header.",
            "type": "Contact Info",
            "impact": "High"
        })
    if contact_gaps.get("phone"):
        phase1_tasks.append({
            "task": "Include an active phone number with country/area code.",
            "type": "Contact Info",
            "impact": "High"
        })
    if contact_gaps.get("links"):
        phase1_tasks.append({
            "task": "Add clickable links to your LinkedIn profile and GitHub or Portfolio website.",
            "type": "Links & Portfolio",
            "impact": "High"
        })

    for sec in missing_sections:
        phase1_tasks.append({
            "task": f"Create a dedicated, clearly labeled section for '{sec}'.",
            "type": "Section Missing",
            "impact": "Critical"
        })

    if missing_vals.get("lacks_quantifiable_metrics", False):
        phase1_tasks.append({
            "task": "Rewrite at least 4 bullet points to include exact numbers, % improvements, or volume (e.g., 'Reduced response time by 40%').",
            "type": "Impact Metrics",
            "impact": "High"
        })

    if missing_vals.get("lacks_action_verbs", False):
        phase1_tasks.append({
            "task": "Replace passive verbs ('was responsible for') with power action verbs ('Spearheaded', 'Engineered', 'Optimized').",
            "type": "ATS Language",
            "impact": "Medium"
        })

    for issue in formatting_issues:
        phase1_tasks.append({
            "task": f"Formatting correction: {issue}",
            "type": "Formatting",
            "impact": "Medium"
        })

    # Default tasks if resume is already clean
    if not phase1_tasks:
        phase1_tasks.append({
            "task": "Perform a final typography and spacing check to ensure standard 10-12pt font hierarchy.",
            "type": "Polish",
            "impact": "Low"
        })
        phase1_tasks.append({
            "task": "Verify that all hyperlinks open valid live projects or active profiles.",
            "type": "Verification",
            "impact": "Medium"
        })

    phases.append({
        "phase_number": 1,
        "title": "Phase 1: Immediate Resume Optimization & Gap Elimination",
        "duration": "1 – 3 Days",
        "description": "Fix formatting bottlenecks, supply missing contact links, and structure essential resume sections.",
        "tasks": phase1_tasks
    })

    # ==================== PHASE 2: TARGETED SKILL ACQUISITION (Weeks 1 - 3) ====================
    phase2_tasks = []
    top_skills_to_learn = missing_skills[:6] if missing_skills else ["advanced cloud concepts", "system architecture", "automated testing"]

    for skill in top_skills_to_learn:
        skill_key = skill.lower()
        guide = SKILL_LEARNING_GUIDES.get(skill_key, {
            "title": f"Mastery of {skill.title()}",
            "resources": [f"Official documentation for {skill}", f"Top-rated crash course on freeCodeCamp / Coursera", f"Hands-on exercises for {skill}"],
            "project": f"Create a mini-project implementing {skill} to demonstrate practical competence."
        })
        phase2_tasks.append({
            "skill": skill.title(),
            "objective": guide["title"],
            "resources": guide["resources"],
            "duration": "3 - 5 Days per skill"
        })

    phases.append({
        "phase_number": 2,
        "title": "Phase 2: Core Missing Skills Mastery",
        "duration": "2 – 3 Weeks",
        "description": "Systematically learn and practice the critical domain skills currently absent from your resume.",
        "skills_plan": phase2_tasks
    })

    # ==================== PHASE 3: PORTFOLIO & PROOF-OF-WORK (Weeks 3 - 5) ====================
    phase3_projects = []
    
    # Generate project ideas incorporating the missing skills
    if missing_skills:
        skill_combos = [missing_skills[i:i+2] for i in range(0, min(len(missing_skills), 4), 2)]
        for idx, combo in enumerate(skill_combos, 1):
            combo_str = " + ".join([s.title() for s in combo])
            phase3_projects.append({
                "project_title": f"Production-Ready Application utilizing {combo_str}",
                "deliverables": [
                    f"Full repository with clean README, architecture diagram, and deployment instructions.",
                    f"Active live demo or recorded Loom walkthrough.",
                    f"Craft 3 resume bullet points highlighting the impact and {combo_str} integration."
                ],
                "recommended_bullet": f"Engineered a scalable system utilizing {combo_str}, cutting execution latency by 35% and serving 1,000+ simulated requests."
            })
    else:
        phase3_projects.append({
            "project_title": "Enterprise Full-Stack Architecture",
            "deliverables": [
                "Implement automated CI/CD pipeline and comprehensive unit/integration test coverage.",
                "Deploy on cloud infrastructure with monitoring and metrics dashboard."
            ],
            "recommended_bullet": "Spearheaded design and deployment of enterprise application, achieving 99.9% uptime and streamlining user onboarding by 45%."
        })

    phases.append({
        "phase_number": 3,
        "title": "Phase 3: Proof-of-Skill Portfolio Projects",
        "duration": "2 – 3 Weeks",
        "description": "Build high-impact, tangible projects that prove competence in the newly acquired skills.",
        "projects": phase3_projects
    })

    # ==================== PHASE 4: CERTIFICATION, ATS RESCAN & APPLICATIONS (Week 6) ====================
    phase4_steps = [
        {
            "step": "Select 1 recognized industry certification (e.g., AWS Certified Cloud Practitioner, GitHub Foundations, or Domain Specialization).",
            "timeline": "Days 1–7"
        },
        {
            "step": "Update your resume with the new projects, skills, and quantifiable achievements using HireLens Resume Maker.",
            "timeline": "Day 8"
        },
        {
            "step": "Re-run the HireLens ATS Checker to verify your score has reached 88% - 98%.",
            "timeline": "Day 9"
        },
        {
            "step": "Target and apply for the matched jobs in your City/State on the HireLens Job Opportunities board.",
            "timeline": "Day 10+"
        }
    ]

    phases.append({
        "phase_number": 4,
        "title": "Phase 4: ATS Validation, Certification & Job Applications",
        "duration": "1 – 2 Weeks",
        "description": "Validate your elevated profile, obtain credentials, and begin targeted job outreach.",
        "steps": phase4_steps
    })

    return {
        "candidate_name": candidate_name,
        "target_category": target_category,
        "current_score": ats_analysis_result.get("overall_score", 60.0),
        "target_score": 95.0,
        "missing_skills_count": len(missing_skills),
        "phases": phases
    }
