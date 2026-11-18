"""
HireLens AI - Comprehensive Universal Skills Taxonomy
Includes Technical, Soft, Leadership, Analytical, Business, and Domain-Specific Skills.
Covers all 24 Kaggle categories and universal professional proficiencies.
"""

SKILL_CATEGORIES = {
    "Technical & Software": [
        # Programming & Scripting
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "r", "scala", "dart", "c",
        # Web Development & Frameworks
        "html", "css", "react", "angular", "vue", "next.js", "node.js", "fastapi", "django", "flask", "spring boot", "express.js", "tailwind css", "bootstrap", "web development", "software development", "frontend", "backend", "full stack",
        # Databases & Storage
        "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle", "sqlite", "graphql", "rest api", "soap", "database management", "database administration",
        # Data Science, AI & Machine Learning
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "machine learning", "deep learning", "nlp", "computer vision", "llms", "data analysis", "data engineering", "big data", "hadoop", "spark", "tableau", "powerbi", "statistics", "data visualization",
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "git", "github", "gitlab", "linux", "unix", "bash", "powershell", "jenkins", "ansible", "cloud computing", "devops", "system administration",
        # Cybersecurity
        "cybersecurity", "penetration testing", "network security", "siem", "firewalls", "cryptography", "identity management", "incident response", "vulnerability assessment", "information security",
        # Engineering & Hardware
        "cad", "autocad", "solidworks", "catia", "matlab", "ansys", "plc programming", "embedded systems", "iot", "robotics", "fe analysis", "pcb design", "hardware", "circuit design",
        # Office & Productivity Software
        "excel", "microsoft excel", "advanced excel", "vlookup", "pivot tables", "word", "microsoft word", "powerpoint", "microsoft powerpoint", "ms office", "microsoft office", "office 365", "google workspace", "google sheets", "google docs", "google slides", "outlook", "slack", "zoom", "teams", "microsoft teams", "trello", "jira", "asana", "notion", "monday.com"
    ],

    "Soft & Interpersonal": [
        "communication", "written communication", "verbal communication", "active listening", "presentation skills", "presentation", "public speaking", "storytelling",
        "teamwork", "collaboration", "cross-functional collaboration", "interpersonal skills", "relationship building", "empathy", "emotional intelligence",
        "conflict resolution", "negotiation", "persuasion", "diplomacy", "cultural awareness", "networking", "client relations",
        "adaptability", "flexibility", "resilience", "growth mindset", "open-mindedness",
        "time management", "organization", "multitasking", "prioritization", "work ethic", "punctuality", "self-motivation", "stress management", "patience"
    ],

    "Leadership & Management": [
        "leadership", "team leadership", "executive leadership", "management", "general management", "team management", "supervision", "operations management", "office administration", "administration",
        "strategic planning", "strategy", "business strategy", "growth strategy", "strategic thinking", "change management", "decision making",
        "project management", "program management", "agile", "scrum", "kanban", "waterfall", "pmp", "scrum master",
        "mentoring", "coaching", "talent development", "delegation", "performance management", "team building",
        "stakeholder management", "vendor management", "resource allocation", "budgeting", "cost control", "p&l management", "p&l",
        "process optimization", "process improvement", "continuous improvement", "lean six sigma", "kaizen", "quality assurance", "quality management"
    ],

    "Analytical & Problem Solving": [
        "problem solving", "critical thinking", "analytical skills", "root cause analysis", "troubleshooting",
        "research", "market research", "quantitative analysis", "qualitative analysis", "data-driven decision making",
        "attention to detail", "accuracy", "pattern recognition", "logical reasoning", "conceptual thinking", "risk assessment", "feasibility analysis",
        "reporting", "business analysis"
    ],

    "Business, Sales & Marketing": [
        "marketing", "digital marketing", "content marketing", "brand management", "product marketing", "marketing strategy", "campaign management", "advertising", "media buying", "social media", "social media marketing", "seo", "sem", "google ads", "google analytics", "email marketing", "content strategy", "copywriting", "public relations", "pr", "growth hacking", "brand awareness",
        "sales", "b2b sales", "b2c sales", "inside sales", "field sales", "retail sales", "direct sales", "enterprise sales", "cold calling", "lead generation", "pipeline management", "account management", "client acquisition", "closing deals", "pitching", "sales management", "revenue growth",
        "crm", "salesforce", "hubspot", "customer service", "customer support", "customer satisfaction", "customer retention", "customer experience", "cx", "client management", "relationship management", "account executive",
        "business development", "strategic partnerships", "market expansion", "competitive analysis", "customer success", "value proposition", "merchandising", "e-commerce", "contract negotiation", "business administration"
    ],

    "HR, People & Operations": [
        "human resources", "hr", "recruitment", "talent acquisition", "sourcing", "technical recruiting", "interviewing", "candidate screening",
        "onboarding", "employee relations", "performance reviews", "hrms", "workday", "bamboohr", "payroll", "payroll administration",
        "labor laws", "compliance", "diversity and inclusion", "dei", "compensation and benefits", "employee engagement", "retention strategies", "workforce planning", "people operations"
    ],

    "Finance, Accounting & Banking": [
        "finance", "accounting", "bookkeeping", "financial analysis", "financial reporting", "financial modeling", "valuation", "dcf", "lbo", "budgeting", "forecasting", "variance analysis",
        "gaap", "ifrs", "general ledger", "balance sheet", "p&l statement", "financial statements", "accounts payable", "accounts receivable", "reconciliation", "bank reconciliation",
        "quickbooks", "tally", "sap", "erp", "auditing", "internal audit", "taxation", "tax preparation", "tax compliance", "gst", "invoicing", "cash flow management",
        "credit analysis", "risk management", "wealth management", "portfolio management", "capital markets", "investment banking", "kyc", "aml", "retail banking", "commercial banking"
    ],

    "Healthcare & Medical": [
        "patient care", "clinical trials", "medical terminology", "emr", "ehr", "epic", "cerner", "nursing", "triage",
        "patient safety", "infection control", "hipaa compliance", "healthcare administration", "bls", "acls", "cpr", "phlebotomy", "clinical documentation", "pharmacology", "vital signs"
    ],

    "Design & Creative": [
        "design", "ui/ux", "figma", "adobe xd", "photoshop", "adobe photoshop", "illustrator", "indesign", "graphic design", "visual design", "interaction design",
        "wireframing", "prototyping", "user research", "usability testing", "design systems", "typography", "branding", "creative direction",
        "video editing", "premiere pro", "after effects", "motion graphics", "animation", "fashion design", "textiles", "apparel design"
    ],

    "Education & Instruction": [
        "teaching", "curriculum development", "lesson planning", "classroom management", "pedagogy", "student assessment", "grading",
        "tutoring", "instructional design", "e-learning", "lms", "educational technology", "academic advising", "special education", "higher education"
    ],

    "Legal, Compliance & Policy": [
        "legal research", "legal drafting", "contract negotiation", "contract management", "litigation", "corporate law",
        "intellectual property", "patents", "trademarks", "regulatory compliance", "arbitration", "due diligence", "ethics", "legal compliance", "dispute resolution"
    ],

    "Hospitality, Fitness & Culinary": [
        "culinary arts", "cooking", "menu planning", "food safety", "haccp", "kitchen management", "fine dining", "catering", "recipe development", "food preparation",
        "fitness", "personal training", "fitness coaching", "strength training", "nutrition", "kinesiology", "wellness coaching", "exercise physiology", "injury prevention"
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
    "ACCOUNTANT": [
        "accounting", "gaap", "general ledger", "balance sheet", "taxation", "auditing", "quickbooks", "excel", "reconciliation", "financial statements",
        "accuracy", "attention to detail", "integrity", "regulatory compliance", "analytical skills", "time management"
    ],
    "ADVOCATE": [
        "legal research", "litigation", "contracts", "corporate law", "due diligence", "legal drafting", "regulatory compliance",
        "negotiation", "persuasion", "critical thinking", "analytical skills", "public speaking", "ethics", "dispute resolution"
    ],
    "AGRICULTURE": [
        "crop management", "agronomy", "soil science", "irrigation", "sustainable farming", "pest control", "precision agriculture",
        "problem solving", "environmental awareness", "resource allocation", "resilience", "operations management", "teamwork"
    ],
    "APPAREL": [
        "fashion design", "textiles", "illustrator", "pattern making", "garment manufacturing", "trend forecasting", "sourcing",
        "creative vision", "aesthetic sense", "vendor management", "attention to detail", "collaboration", "market research"
    ],
    "ARTS": [
        "fine arts", "illustration", "curation", "visual arts", "digital art", "photoshop", "exhibition planning",
        "creative expression", "visual storytelling", "concept thinking", "patience", "adaptability", "collaboration"
    ],
    "AUTOMOBILE": [
        "automotive engineering", "diagnostics", "engine repair", "cad/cam", "powertrain", "vehicle dynamics", "quality assurance",
        "troubleshooting", "mechanical aptitude", "safety consciousness", "teamwork", "continuous improvement", "problem solving"
    ],
    "AVIATION": [
        "flight operations", "aircraft maintenance", "faa regulations", "avionics", "navigation", "safety management systems",
        "crew resource management", "situational awareness", "crisis management", "decisiveness", "communication", "team leadership"
    ],
    "BANKING": [
        "credit analysis", "risk management", "wealth management", "kyc", "aml", "retail banking", "portfolio management",
        "relationship building", "trust building", "integrity", "communication", "decision making", "attention to detail"
    ],
    "BPO": [
        "customer support", "customer service", "crm", "ticketing systems", "telecalling", "call quality", "kpi management", "inbound and outbound",
        "active listening", "patience", "empathy", "conflict resolution", "verbal communication", "problem solving", "adaptability"
    ],
    "BUSINESS-DEVELOPMENT": [
        "business development", "marketing", "business strategy", "strategic partnerships", "b2b sales", "lead generation", "crm", "salesforce", "customer service", "market research", "revenue growth",
        "relationship building", "negotiation", "strategic planning", "leadership", "management", "communication", "presentation skills"
    ],
    "CHEF": [
        "culinary arts", "menu planning", "food safety", "haccp", "kitchen management", "recipe development", "inventory control",
        "creativity", "attention to detail", "stress management", "team leadership", "multitasking", "time management"
    ],
    "CONSTRUCTION": [
        "autocad", "bim", "blueprints", "project estimation", "site supervision", "osha safety", "budgeting",
        "leadership", "worker safety", "vendor negotiation", "conflict resolution", "problem solving", "decision making"
    ],
    "CONSULTANT": [
        "management consulting", "process optimization", "financial analysis", "market research", "lean six sigma", "kpi development",
        "strategic planning", "problem solving", "stakeholder management", "change management", "presentation skills", "executive leadership"
    ],
    "DESIGNER": [
        "figma", "ui/ux", "adobe photoshop", "illustrator", "wireframing", "prototyping", "design systems", "typography",
        "user research", "creative problem solving", "visual storytelling", "cross-functional collaboration", "empathy", "presentation skills"
    ],
    "DIGITAL-MEDIA": [
        "marketing", "digital marketing", "social media marketing", "social media", "seo", "sem", "google analytics", "content strategy", "video editing", "copywriting",
        "creative storytelling", "brand management", "audience empathy", "trend awareness", "cross-functional collaboration", "adaptability"
    ],
    "ENGINEERING": [
        "cad", "solidworks", "matlab", "structural analysis", "quality control", "lean manufacturing", "prototyping", "fe analysis",
        "problem solving", "root cause analysis", "cross-functional collaboration", "project management", "teamwork", "analytical skills"
    ],
    "FINANCE": [
        "finance", "financial modeling", "valuation", "dcf", "budgeting", "forecasting", "variance analysis", "financial analysis", "powerbi", "excel",
        "critical thinking", "attention to detail", "risk assessment", "strategic planning", "stakeholder management", "executive presentation"
    ],
    "FITNESS": [
        "fitness", "personal training", "strength training", "nutrition", "kinesiology", "cpr", "exercise physiology", "injury prevention",
        "client motivation", "empathy", "active listening", "interpersonal skills", "goal setting", "patience", "communication"
    ],
    "HEALTHCARE": [
        "patient care", "clinical trials", "emr", "ehr", "hipaa compliance", "medical terminology", "nursing", "bls",
        "empathy", "patient safety", "communication", "critical thinking", "multitasking", "stress management", "collaboration"
    ],
    "HR": [
        "human resources", "talent acquisition", "recruitment", "onboarding", "hrms", "payroll administration", "labor laws", "compensation and benefits",
        "employee relations", "interpersonal skills", "conflict resolution", "active listening", "empathy", "performance management", "diversity and inclusion"
    ],
    "INFORMATION-TECHNOLOGY": [
        "python", "sql", "aws", "docker", "kubernetes", "react", "ci/cd", "git", "linux", "rest api", "cloud computing",
        "problem solving", "troubleshooting", "agile", "teamwork", "communication", "adaptability", "continuous improvement"
    ],
    "PUBLIC-RELATIONS": [
        "public relations", "press releases", "media relations", "crisis communication", "branding", "event planning", "social media",
        "public speaking", "storytelling", "interpersonal skills", "relationship building", "persuasion", "crisis response"
    ],
    "SALES": [
        "sales", "pipeline management", "b2b sales", "crm", "salesforce", "lead generation", "cold calling", "account management", "customer service",
        "closing deals", "negotiation", "persuasion", "relationship building", "active listening", "resilience", "presentation skills"
    ],
    "TEACHER": [
        "teaching", "curriculum development", "lesson planning", "student assessment", "instructional design", "pedagogy", "educational technology",
        "classroom management", "communication", "public speaking", "empathy", "mentoring", "patience", "active listening"
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
