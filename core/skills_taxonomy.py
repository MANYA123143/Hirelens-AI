"""
HireLens AI - Comprehensive Universal Skills Taxonomy
Includes Technical, Soft, Leadership, Analytical, Business, and Domain-Specific Skills.
"""

SKILL_CATEGORIES = {
    "Technical & Software": [
        # Programming & Scripting
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "r", "scala", "dart",
        # Web Development & Frameworks
        "html", "css", "react", "angular", "vue", "next.js", "node.js", "fastapi", "django", "flask", "spring boot", "express.js", "tailwind css", "bootstrap",
        # Databases & Storage
        "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle", "sqlite", "graphql", "rest api", "soap",
        # Data Science, AI & Machine Learning
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "machine learning", "deep learning", "nlp", "computer vision", "llms", "data analysis", "data engineering", "big data", "hadoop", "spark", "tableau", "powerbi", "statistics",
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "git", "github", "gitlab", "linux", "unix", "bash", "powershell", "jenkins", "ansible", "cloud computing",
        # Cybersecurity
        "cybersecurity", "penetration testing", "network security", "siem", "firewalls", "cryptography", "identity management", "incident response", "vulnerability assessment",
        # Engineering & Hardware
        "cad", "autocad", "solidworks", "catia", "matlab", "ansys", "plc programming", "embedded systems", "iot", "robotics", "fe analysis", "pcb design"
    ],

    "Soft & Interpersonal": [
        "communication", "written communication", "verbal communication", "active listening", "presentation skills", "public speaking", "storytelling",
        "teamwork", "collaboration", "cross-functional collaboration", "interpersonal skills", "relationship building", "empathy", "emotional intelligence",
        "conflict resolution", "negotiation", "persuasion", "diplomacy", "cultural awareness", "networking",
        "adaptability", "flexibility", "resilience", "growth mindset", "open-mindedness",
        "time management", "organization", "multitasking", "prioritization", "work ethic", "punctuality", "self-motivation", "stress management", "patience"
    ],

    "Leadership & Management": [
        "leadership", "team leadership", "executive leadership", "strategic planning", "change management", "decision making",
        "project management", "program management", "agile", "scrum", "kanban", "waterfall", "jira", "pmp", "scrum master",
        "mentoring", "coaching", "talent development", "delegation", "performance management", "team building",
        "stakeholder management", "vendor management", "resource allocation", "budgeting", "cost control", "p&l management",
        "operations management", "process optimization", "continuous improvement", "lean six sigma", "kaizen"
    ],

    "Analytical & Problem Solving": [
        "problem solving", "critical thinking", "analytical skills", "root cause analysis", "troubleshooting",
        "research", "market research", "quantitative analysis", "qualitative analysis", "data-driven decision making",
        "attention to detail", "accuracy", "pattern recognition", "logical reasoning", "conceptual thinking", "risk assessment", "feasibility analysis"
    ],

    "Business, Sales & Marketing": [
        "b2b sales", "b2c sales", "crm", "salesforce", "hubspot", "lead generation", "cold calling", "pipeline management", "account management", "client acquisition", "closing deals",
        "digital marketing", "seo", "sem", "google ads", "google analytics", "social media marketing", "email marketing", "content strategy", "copywriting", "brand management", "public relations", "growth hacking",
        "business development", "strategic partnerships", "revenue growth", "market expansion", "competitive analysis", "customer success", "customer retention", "value proposition", "pitching"
    ],

    "HR, People & Operations": [
        "recruitment", "talent acquisition", "sourcing", "technical recruiting", "interviewing", "candidate screening",
        "onboarding", "employee relations", "performance reviews", "hrms", "workday", "bamboohr", "payroll administration",
        "labor laws", "compliance", "diversity and inclusion", "compensation and benefits", "employee engagement", "retention strategies", "workforce planning"
    ],

    "Finance, Accounting & Banking": [
        "financial modeling", "valuation", "dcf", "lbo", "budgeting", "forecasting", "financial analysis", "variance analysis",
        "gaap", "ifrs", "accounting", "general ledger", "balance sheet", "accounts payable", "accounts receivable", "reconciliation",
        "quickbooks", "tally", "sap", "auditing", "internal audit", "taxation", "tax compliance", "gst",
        "credit analysis", "risk management", "wealth management", "portfolio management", "capital markets", "investment banking", "kyc", "aml"
    ],

    "Healthcare & Medical": [
        "patient care", "clinical trials", "medical terminology", "emr", "ehr", "epic", "cerner", "nursing", "triage",
        "patient safety", "infection control", "hipaa compliance", "healthcare administration", "bls", "acls", "cpr", "phlebotomy", "clinical documentation"
    ],

    "Design & Creative": [
        "ui/ux", "figma", "adobe xd", "photoshop", "illustrator", "indesign", "graphic design", "visual design", "interaction design",
        "wireframing", "prototyping", "user research", "usability testing", "design systems", "typography", "branding",
        "video editing", "premiere pro", "after effects", "motion graphics", "animation", "creative direction", "fashion design", "textiles"
    ],

    "Education & Instruction": [
        "curriculum development", "lesson planning", "classroom management", "pedagogy", "student assessment", "grading",
        "tutoring", "instructional design", "e-learning", "lms", "educational technology", "academic advising", "special education"
    ],

    "Legal, Compliance & Policy": [
        "legal research", "legal drafting", "contract negotiation", "contract management", "litigation", "corporate law",
        "intellectual property", "patents", "trademarks", "regulatory compliance", "arbitration", "due diligence", "ethics"
    ],

    "Hospitality, Fitness & Culinary": [
        "culinary arts", "menu planning", "food safety", "haccp", "kitchen management", "fine dining", "catering", "recipe development",
        "personal training", "fitness coaching", "strength training", "nutrition", "kinesiology", "wellness coaching", "exercise physiology"
    ]
}

# Flattened list of ALL unique skills for rapid O(1) keyword detection
ALL_SKILLS_LIST = []
SKILL_TO_CATEGORY_MAP = {}
for category_name, skills_in_cat in SKILL_CATEGORIES.items():
    for sk in skills_in_cat:
        sk_lower = sk.lower().strip()
        if sk_lower not in SKILL_TO_CATEGORY_MAP:
            ALL_SKILLS_LIST.append(sk_lower)
            SKILL_TO_CATEGORY_MAP[sk_lower] = category_name

# Balanced Technical + Non-Technical Skills for all 24 Kaggle Categories
CATEGORY_BENCHMARK_SKILLS = {
    "HR": [
        "talent acquisition", "recruitment", "onboarding", "hrms", "payroll administration", "labor laws", "compensation and benefits",
        "employee relations", "interpersonal skills", "conflict resolution", "active listening", "empathy", "performance management", "diversity and inclusion"
    ],
    "DESIGNER": [
        "figma", "ui/ux", "adobe photoshop", "illustrator", "wireframing", "prototyping", "design systems", "typography",
        "user research", "creative problem solving", "visual storytelling", "cross-functional collaboration", "empathy", "presentation skills"
    ],
    "INFORMATION-TECHNOLOGY": [
        "python", "sql", "aws", "docker", "kubernetes", "react", "ci/cd", "git", "linux", "rest api", "cloud computing",
        "problem solving", "troubleshooting", "agile", "teamwork", "communication", "adaptability", "continuous improvement"
    ],
    "TEACHER": [
        "curriculum development", "lesson planning", "student assessment", "instructional design", "pedagogy", "educational technology",
        "classroom management", "communication", "public speaking", "empathy", "mentoring", "patience", "active listening"
    ],
    "ADVOCATE": [
        "legal research", "litigation", "contracts", "corporate law", "due diligence", "legal drafting", "regulatory compliance",
        "negotiation", "persuasion", "critical thinking", "analytical skills", "public speaking", "ethics", "dispute resolution"
    ],
    "BUSINESS-DEVELOPMENT": [
        "strategic partnerships", "b2b sales", "lead generation", "crm", "salesforce", "market research", "revenue growth",
        "relationship building", "negotiation", "networking", "persuasion", "strategic planning", "executive leadership", "communication"
    ],
    "HEALTHCARE": [
        "patient care", "clinical trials", "emr", "ehr", "hipaa compliance", "medical terminology", "nursing", "bls",
        "empathy", "patient safety", "communication", "critical thinking", "multitasking", "stress management", "collaboration"
    ],
    "FITNESS": [
        "personal training", "strength training", "nutrition", "kinesiology", "cpr", "exercise physiology", "injury prevention",
        "client motivation", "empathy", "active listening", "interpersonal skills", "goal setting", "patience", "communication"
    ],
    "AGRICULTURE": [
        "crop management", "agronomy", "soil science", "irrigation", "sustainable farming", "pest control", "precision agriculture",
        "problem solving", "environmental awareness", "resource allocation", "resilience", "operations management", "teamwork"
    ],
    "BPO": [
        "customer support", "crm", "ticketing systems", "telecalling", "call quality", "kpi management", "inbound and outbound",
        "active listening", "patience", "empathy", "conflict resolution", "verbal communication", "problem solving", "adaptability"
    ],
    "SALES": [
        "pipeline management", "b2b sales", "crm", "salesforce", "lead generation", "cold calling", "account management",
        "closing deals", "negotiation", "persuasion", "relationship building", "active listening", "resilience", "presentation skills"
    ],
    "CONSULTANT": [
        "management consulting", "process optimization", "financial analysis", "market research", "lean six sigma", "kpi development",
        "strategic planning", "problem solving", "stakeholder management", "change management", "presentation skills", "executive leadership"
    ],
    "DIGITAL-MEDIA": [
        "seo", "sem", "social media marketing", "google analytics", "content strategy", "video editing", "copywriting",
        "creative storytelling", "brand management", "audience empathy", "trend awareness", "cross-functional collaboration", "adaptability"
    ],
    "AUTOMOBILE": [
        "automotive engineering", "diagnostics", "engine repair", "cad/cam", "powertrain", "vehicle dynamics", "quality assurance",
        "troubleshooting", "mechanical aptitude", "safety consciousness", "teamwork", "continuous improvement", "problem solving"
    ],
    "CHEF": [
        "culinary arts", "menu planning", "food safety", "haccp", "kitchen management", "recipe development", "inventory control",
        "creativity", "attention to detail", "stress management", "team leadership", "multitasking", "time management"
    ],
    "FINANCE": [
        "financial modeling", "valuation", "dcf", "budgeting", "forecasting", "variance analysis", "financial analysis", "powerbi",
        "critical thinking", "attention to detail", "risk assessment", "strategic planning", "stakeholder management", "executive presentation"
    ],
    "APPAREL": [
        "fashion design", "textiles", "illustrator", "pattern making", "garment manufacturing", "trend forecasting", "sourcing",
        "creative vision", "aesthetic sense", "vendor management", "attention to detail", "collaboration", "market research"
    ],
    "ENGINEERING": [
        "cad", "solidworks", "matlab", "structural analysis", "quality control", "lean manufacturing", "prototyping", "fe analysis",
        "problem solving", "root cause analysis", "cross-functional collaboration", "project management", "teamwork", "analytical skills"
    ],
    "ACCOUNTANT": [
        "gaap", "general ledger", "taxation", "auditing", "quickbooks", "tally", "reconciliation", "financial statements",
        "accuracy", "attention to detail", "integrity", "organization", "regulatory compliance", "analytical skills", "time management"
    ],
    "CONSTRUCTION": [
        "autocad", "bim", "blueprints", "project estimation", "site supervision", "osha safety", "budgeting",
        "leadership", "worker safety", "vendor negotiation", "conflict resolution", "problem solving", "decision making"
    ],
    "PUBLIC-RELATIONS": [
        "press releases", "media relations", "crisis communication", "branding", "event planning", "social media marketing",
        "public speaking", "storytelling", "interpersonal skills", "relationship building", "persuasion", "crisis response"
    ],
    "BANKING": [
        "credit analysis", "risk management", "wealth management", "kyc", "aml", "retail banking", "portfolio management",
        "relationship building", "trust building", "integrity", "communication", "decision making", "attention to detail"
    ],
    "ARTS": [
        "fine arts", "illustration", "curation", "visual arts", "digital art", "photoshop", "exhibition planning",
        "creative expression", "visual storytelling", "concept thinking", "patience", "adaptability", "collaboration"
    ],
    "AVIATION": [
        "flight operations", "aircraft maintenance", "faa regulations", "avionics", "navigation", "safety management systems",
        "crew resource management", "situational awareness", "crisis management", "decisiveness", "communication", "team leadership"
    ]
}

def classify_skill(skill: str) -> str:
    """Returns the primary category for any given skill."""
    return SKILL_TO_CATEGORY_MAP.get(skill.lower().strip(), "Professional Skill")

def get_skills_for_category(category_name: str) -> list[str]:
    """Returns benchmark skills for a specific Kaggle category."""
    cat_upper = category_name.upper().strip()
    return CATEGORY_BENCHMARK_SKILLS.get(cat_upper, [
        "communication", "teamwork", "problem solving", "leadership", "time management", "analytical skills", "project management"
    ])
