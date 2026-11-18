"""
HireLens AI - Missing Values & Skills Career Roadmap Generator
Constructs a personalized 4-phase learning and portfolio roadmap to bridge identified resume gaps.
Supports both Technical and Non-Technical / Soft / Leadership skills.
"""

# Resource and project guides mapped to commonly missing skills (Technical + Non-Technical)
SKILL_LEARNING_GUIDES = {
    # Technical Skills
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
    },

    # Non-Technical & Soft Skills
    "communication": {
        "title": "Executive Communication & Technical Storytelling",
        "resources": ["Think Fast, Talk Smart (Stanford GSB)", "Harvard Business Review Guide to Persuasive Presentations", "Toastmasters Public Speaking Guides"],
        "project": "Draft a formal technical executive summary and slide deck explaining a complex system to non-technical stakeholders."
    },
    "leadership": {
        "title": "Modern Team Leadership & Influence",
        "resources": ["The Making of a Manager by Julie Zhuo", "Radical Candor Framework", "Coursera Strategic Leadership Specialization"],
        "project": "Develop a structured operational leadership playbook covering team 1-on-1s, OKRs, and constructive feedback rubrics."
    },
    "problem solving": {
        "title": "Structured Problem Solving & Root Cause Analysis",
        "resources": ["McKinsey 7-Step Problem Solving Framework", "The 5 Whys & Ishikawa Diagram Method", "Critical Thinking for Decision Makers"],
        "project": "Conduct an in-depth post-mortem investigation on a simulated operational bottleneck and document preventative SOPs."
    },
    "teamwork": {
        "title": "Cross-Functional Collaboration & Team Dynamics",
        "resources": ["Google's Project Aristotle on Psychological Safety", "Atlassian Team Playbook", "Crucial Conversations"],
        "project": "Coordinate a cross-disciplinary team charter establishing code-review SLAs, meeting etiquette, and shared goals."
    },
    "negotiation": {
        "title": "High-Stakes Business Negotiation & Influence",
        "resources": ["Never Split the Difference by Chris Voss", "Harvard Program on Negotiation (PON)", "Getting to Yes Framework"],
        "project": "Formulate a vendor procurement negotiation matrix outlining BATNA, trade-offs, and risk allocation terms."
    },
    "time management": {
        "title": "High-Velocity Prioritization & Execution",
        "resources": ["Getting Things Done (GTD) Method", "Deep Work Principles by Cal Newport", "Eisenhower Matrix Prioritization"],
        "project": "Design an automated personal task triage board categorizing work by urgency and impact with weekly review cadences."
    },
    "active listening": {
        "title": "Active Listening & Stakeholder Empathy",
        "resources": ["Nonviolent Communication by Marshall Rosenberg", "Harvard Program on Negotiation Listening Labs", "MindTools Active Listening"],
        "project": "Execute 5 stakeholder discovery interviews, synthesizing key unstated pain points into actionable feature requirements."
    },
    "conflict resolution": {
        "title": "Workplace Conflict Resolution & De-escalation",
        "resources": ["Thomas-Kilmann Conflict Mode Instrument", "Crucial Conversations Methodology", "Mediation & Dispute Resolution Guides"],
        "project": "Draft a conflict resolution protocol for addressing technical architectural disagreements productively."
    },
    "agile": {
        "title": "Agile Delivery & Scrum Orchestration",
        "resources": ["Official Scrum Guide (scrumguides.org)", "Atlassian Agile Coach", "Google Agile Project Management Course"],
        "project": "Set up a Jira/GitHub Projects sprint board with user stories, acceptance criteria, and burndown chart metrics."
    }
}

def generate_missing_values_roadmap(ats_analysis_result: dict, candidate_name: str = "Candidate", target_category: str = "Target Domain") -> dict:
    """
    Constructs a detailed 4-phase step-by-step roadmap to eliminate missing values,
    acquire missing technical and non-technical skills, and maximize ATS score.
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
            "task": "Replace passive verbs ('was responsible for') with power action verbs ('Spearheaded', 'Engineered', 'Optimized', 'Negotiated').",
            "type": "ATS Language",
            "impact": "Medium"
        })

    for issue in formatting_issues:
        phase1_tasks.append({
            "task": f"Formatting correction: {issue}",
            "type": "Formatting",
            "impact": "Medium"
        })

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
    top_skills_to_learn = missing_skills[:8] if missing_skills else ["communication", "problem solving", "leadership", "agile", "cloud computing"]

    for skill in top_skills_to_learn:
        skill_key = skill.lower()
        guide = SKILL_LEARNING_GUIDES.get(skill_key, {
            "title": f"Mastery of {skill.title()}",
            "resources": [f"Curated guides & best practices for {skill}", f"Interactive masterclass on Coursera / YouTube", f"Practical application exercise for {skill}"],
            "project": f"Create a concrete deliverable implementing {skill} to demonstrate practical competence."
        })
        phase2_tasks.append({
            "skill": skill.title(),
            "objective": guide["title"],
            "resources": guide["resources"],
            "duration": "3 - 5 Days per skill"
        })

    phases.append({
        "phase_number": 2,
        "title": "Phase 2: Core Missing Skills Mastery (Technical & Soft)",
        "duration": "2 – 3 Weeks",
        "description": "Systematically learn and practice both hard technical and essential soft/leadership skills currently absent from your resume.",
        "skills_plan": phase2_tasks
    })

    # ==================== PHASE 3: PORTFOLIO & PROOF-OF-WORK (Weeks 3 - 5) ====================
    phase3_projects = []
    
    if missing_skills:
        skill_combos = [missing_skills[i:i+2] for i in range(0, min(len(missing_skills), 6), 2)]
        for idx, combo in enumerate(skill_combos, 1):
            combo_str = " + ".join([s.title() for s in combo])
            phase3_projects.append({
                "project_title": f"Applied Professional Project utilizing {combo_str}",
                "deliverables": [
                    f"Comprehensive project repository or case study with clear README, deliverables, and measurable outcomes.",
                    f"Active demonstration or interactive artifact proving hands-on mastery of {combo_str}.",
                    f"Craft 3 resume bullet points highlighting the impact and {combo_str} integration."
                ],
                "recommended_bullet": f"Spearheaded initiatives utilizing {combo_str}, cutting cycle times by 30% and elevating team output across multi-disciplinary workflows."
            })
    else:
        phase3_projects.append({
            "project_title": "Enterprise Strategic Execution",
            "deliverables": [
                "Implement end-to-end operational workflows with rigorous quality benchmarks.",
                "Deploy with real-time performance tracking and executive reporting dashboard."
            ],
            "recommended_bullet": "Directed cross-functional execution of core strategic framework, improving operational velocity by 40% and ensuring 100% regulatory compliance."
        })

    phases.append({
        "phase_number": 3,
        "title": "Phase 3: Proof-of-Skill Portfolio Projects",
        "duration": "2 – 3 Weeks",
        "description": "Build high-impact, tangible projects that prove competence in both newly acquired technical tools and soft skills.",
        "projects": phase3_projects
    })

    # ==================== PHASE 4: CERTIFICATION, ATS RESCAN & APPLICATIONS (Week 6) ====================
    phase4_steps = [
        {
            "step": "Obtain 1 recognized credential or certification (e.g. AWS Cloud Practitioner, PMP / Scrum Master, or Domain Specialization).",
            "timeline": "Days 1–7"
        },
        {
            "step": "Update your resume with new technical projects and quantifiable soft skill achievements using HireLens Resume Maker.",
            "timeline": "Day 8"
        },
        {
            "step": "Re-run the HireLens ATS Checker to verify your score has reached 90% - 98%.",
            "timeline": "Day 9"
        },
        {
            "step": "Apply to matched local positions in your City/State on the HireLens Job Opportunities board.",
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
