"""
HireLens AI - Global Jobs Database Seeder
Populates rich worldwide job opportunities across cities, states, and countries.
"""
from database.db import get_connection, insert_job

WORLD_CITIES = {
    # United States
    ("San Francisco", "California", "United States"): (37.7749, -122.4194),
    ("New York", "New York", "United States"): (40.7128, -74.0060),
    ("Seattle", "Washington", "United States"): (47.6062, -122.3321),
    ("Austin", "Texas", "United States"): (30.2672, -97.7431),
    ("Boston", "Massachusetts", "United States"): (42.3601, -71.0589),
    ("Chicago", "Illinois", "United States"): (41.8781, -87.6298),
    ("Los Angeles", "California", "United States"): (34.0522, -118.2437),
    ("Denver", "Colorado", "United States"): (39.7392, -104.9903),
    # India
    ("Bengaluru", "Karnataka", "India"): (12.9716, 77.5946),
    ("Mumbai", "Maharashtra", "India"): (19.0760, 72.8777),
    ("Hyderabad", "Telangana", "India"): (17.3850, 78.4867),
    ("Pune", "Maharashtra", "India"): (18.5204, 73.8567),
    ("New Delhi", "Delhi", "India"): (28.6139, 77.2090),
    ("Chennai", "Tamil Nadu", "India"): (13.0827, 80.2707),
    ("Noida", "Uttar Pradesh", "India"): (28.5355, 77.3910),
    ("Gurugram", "Haryana", "India"): (28.4595, 77.0266),
    # United Kingdom
    ("London", "Greater London", "United Kingdom"): (51.5074, -0.1278),
    ("Manchester", "Greater Manchester", "United Kingdom"): (53.4808, -2.2426),
    ("Edinburgh", "Scotland", "United Kingdom"): (55.9533, -3.1883),
    # Europe
    ("Berlin", "Berlin", "Germany"): (52.5200, 13.4050),
    ("Munich", "Bavaria", "Germany"): (48.1351, 11.5820),
    ("Paris", "Île-de-France", "France"): (48.8566, 2.3522),
    ("Amsterdam", "North Holland", "Netherlands"): (52.3676, 4.9041),
    ("Zurich", "Zurich", "Switzerland"): (47.3769, 8.5417),
    ("Dublin", "Leinster", "Ireland"): (53.3498, -6.2603),
    # Canada
    ("Toronto", "Ontario", "Canada"): (43.6532, -79.3832),
    ("Vancouver", "British Columbia", "Canada"): (49.2827, -123.1207),
    ("Montreal", "Quebec", "Canada"): (45.5017, -73.5673),
    # Asia Pacific & Middle East
    ("Singapore", "Central", "Singapore"): (1.3521, 103.8198),
    ("Tokyo", "Kanto", "Japan"): (35.6762, 139.6503),
    ("Sydney", "New South Wales", "Australia"): (-33.8688, 151.2093),
    ("Melbourne", "Victoria", "Australia"): (-37.8136, 144.9631),
    ("Dubai", "Dubai", "United Arab Emirates"): (25.2048, 55.2708),
    ("Remote", "Global", "Worldwide"): (20.0, 0.0)
}

SAMPLE_JOBS = [
    # --- INFORMATION-TECHNOLOGY ---
    {
        "title": "Senior AI & Machine Learning Engineer",
        "company": "DeepPulse Labs",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$165,000 - $210,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Python, PyTorch, TensorFlow, LLMs, NLP, Docker, AWS, MLOps, SQL",
        "description": "Architect and deploy generative AI pipelines, fine-tune transformer models, and optimize inference latency for enterprise solutions."
    },
    {
        "title": "Full Stack Cloud Developer",
        "company": "Nexus Technologies",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹18,00,000 - ₹28,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Python, React, TypeScript, FastAPI, PostgreSQL, Docker, AWS, Git",
        "description": "Build high-throughput web applications, microservices, and reactive user interfaces for global FinTech clients."
    },
    {
        "title": "DevOps & Cloud Infrastructure Specialist",
        "company": "CloudForge Systems",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$140,000 - $175,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Kubernetes, Docker, Terraform, AWS, CI/CD, Linux, Python, Prometheus",
        "description": "Manage multi-cloud infrastructure, automate zero-downtime deployment pipelines, and strengthen cluster security."
    },
    {
        "title": "Junior Data Scientist & Analyst",
        "company": "DataSphere Analytics",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Hyderabad", "Telangana", "India"),
        "salary_range": "₹9,00,000 - ₹15,00,000",
        "job_type": "Full-time",
        "experience_required": "Fresher / Junior (0-2 yrs)",
        "required_skills": "Python, SQL, Pandas, NumPy, Scikit-learn, Tableau, PowerBI, Statistics",
        "description": "Analyze large customer transaction datasets, develop predictive models, and produce actionable executive dashboards."
    },
    {
        "title": "Backend Distributed Systems Engineer",
        "company": "FinVector",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£80,000 - £105,000",
        "job_type": "Hybrid",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Python, Go, Java, Kafka, Microservices, Redis, PostgreSQL, Distributed Systems",
        "description": "Design resilient trading ledger engines with sub-millisecond execution times and fault-tolerant architecture."
    },
    {
        "title": "Cybersecurity & Incident Response Analyst",
        "company": "SecureNet Global",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Berlin", "Berlin", "Germany"),
        "salary_range": "€75,000 - €95,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Network Security, SIEM, Penetration Testing, Python, Incident Response, ISO 27001",
        "description": "Protect critical enterprise assets, conduct threat hunting, and implement SOC response workflows across EU operations."
    },
    {
        "title": "Mobile App Developer (iOS & Android)",
        "company": "AppFlow Studio",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹12,00,000 - ₹19,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (1-3 yrs)",
        "required_skills": "Flutter, React Native, Swift, Kotlin, REST APIs, Git, Firebase",
        "description": "Create cross-platform mobile apps with silky 60fps animations and offline sync capabilities."
    },
    {
        "title": "Lead Software Architect",
        "company": "OmniGlobal Tech",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$190,000 - $240,000",
        "job_type": "Full-time",
        "experience_required": "Senior (7+ yrs)",
        "required_skills": "System Design, Microservices, Python, Java, Cloud Architecture, Scalability, Mentorship",
        "description": "Spearhead technological roadmap, evaluate emerging frameworks, and lead engineering culture across 5 global teams."
    },
    {
        "title": "Frontend React / UI Engineer",
        "company": "Starlight Interactive",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Toronto", "Ontario", "Canada"),
        "salary_range": "C$95,000 - C$125,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (2-4 yrs)",
        "required_skills": "React, TypeScript, Next.js, Tailwind CSS, Redux, Webpack, Responsive Design",
        "description": "Craft intuitive, accessible SaaS interfaces with blazing fast render speeds and modular design systems."
    },

    # --- DESIGNER ---
    {
        "title": "Senior Product & UI/UX Designer",
        "company": "Aura Design Co",
        "category": "DESIGNER",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$125,000 - $160,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Figma, UI/UX, Wireframing, Prototyping, User Research, Design Systems, Typography",
        "description": "Lead design sprints, develop comprehensive design systems, and partner with product leads to elevate mobile engagement."
    },
    {
        "title": "UI/UX Interaction Designer",
        "company": "Kreative Labs",
        "category": "DESIGNER",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹14,00,000 - ₹22,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-4 yrs)",
        "required_skills": "Figma, Adobe XD, User Journey Mapping, Usability Testing, Visual Design, HTML/CSS basics",
        "description": "Transform complex business workflows into simple, elegant product interfaces and conduct user usability studies."
    },
    {
        "title": "Visual Brand & Graphic Designer",
        "company": "Vivid Media Group",
        "category": "DESIGNER",
        "loc": ("Amsterdam", "North Holland", "Netherlands"),
        "salary_range": "€60,000 - €78,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Adobe Photoshop, Illustrator, Brand Identity, Motion Graphics, Print Design, Figma",
        "description": "Establish cohesive visual identities for pan-European marketing campaigns, presentations, and product packaging."
    },

    # --- FINANCE & BANKING ---
    {
        "title": "Senior Financial Analyst & Modeler",
        "company": "Apex Capital Management",
        "category": "FINANCE",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$135,000 - $170,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Financial Modeling, Valuation, Excel, Budgeting, Forecasting, DCF, PowerBI, SQL",
        "description": "Build sophisticated DCF and LBO valuation models, forecast divisional revenues, and deliver quarterly board presentations."
    },
    {
        "title": "Investment Banking Associate",
        "company": "Centurion Global Bank",
        "category": "BANKING",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹22,00,000 - ₹35,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Mergers & Acquisitions, Financial Analysis, Pitch Books, Due Diligence, Capital Markets",
        "description": "Execute cross-border M&A transactions, evaluate capital structures, and conduct due diligence for Fortune 500 corporations."
    },
    {
        "title": "Wealth Management & Portfolio Advisor",
        "company": "Helvetia Private Bank",
        "category": "BANKING",
        "loc": ("Zurich", "Zurich", "Switzerland"),
        "salary_range": "CHF 120,000 - CHF 155,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Portfolio Management, Wealth Planning, Asset Allocation, Compliance, Client Advisory",
        "description": "Manage multi-asset portfolios for high-net-worth individuals, ensuring tax efficiency and rigorous risk controls."
    },
    {
        "title": "Quantitative Risk Analyst",
        "company": "Sterling Risk Partners",
        "category": "FINANCE",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£75,000 - £98,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Risk Management, Python, Value at Risk (VaR), Stress Testing, Financial Derivatives, SQL",
        "description": "Perform portfolio stress testing, build counterparty risk models, and ensure Basel III regulatory compliance."
    },

    # --- ACCOUNTANT ---
    {
        "title": "Senior Corporate Accountant",
        "company": "Vanguard Accounting Partners",
        "category": "ACCOUNTANT",
        "loc": ("Chicago", "Illinois", "United States"),
        "salary_range": "$85,000 - $110,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "GAAP, General Ledger, Financial Statements, Reconciliation, QuickBooks, ERP, Auditing",
        "description": "Manage monthly financial closing, prepare balance sheet reconciliations, and coordinate external statutory audits."
    },
    {
        "title": "Tax Compliance & Audit Manager",
        "company": "Deloitte & Associates India",
        "category": "ACCOUNTANT",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹14,00,000 - ₹20,00,000",
        "job_type": "Full-time",
        "experience_required": "Senior (4-7 yrs)",
        "required_skills": "Direct & Indirect Tax, GST, Income Tax, Tax Planning, Tally, Auditing, Statutory Compliance",
        "description": "Supervise tax compliance for corporate entities, lead transfer pricing assessments, and liaise with authorities."
    },

    # --- HR (HUMAN RESOURCES) ---
    {
        "title": "Lead Technical Recruiter & Talent Partner",
        "company": "HyperScale Ventures",
        "category": "HR",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$115,000 - $145,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Technical Recruiting, Sourcing, ATS, LinkedIn Recruiter, Interviewing, Offer Negotiation",
        "description": "Drive end-to-end recruitment for high-growth AI and engineering teams from source to onboarding."
    },
    {
        "title": "People Operations & HR Business Partner",
        "company": "Zenith Global Tech",
        "category": "HR",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹12,00,000 - ₹18,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "HR Policies, Employee Relations, Performance Management, HRMS, Talent Development, Retention",
        "description": "Partner with VP of Engineering to design career frameworks, conduct retention reviews, and foster vibrant work culture."
    },
    {
        "title": "Global HR Generalist",
        "company": "Eurasia Mobility",
        "category": "HR",
        "loc": ("Dublin", "Leinster", "Ireland"),
        "salary_range": "€55,000 - €70,000",
        "job_type": "Hybrid",
        "experience_required": "Junior-Mid (2-4 yrs)",
        "required_skills": "Onboarding, Payroll, Employment Law, Employee Engagement, Workday, Benefits Administration",
        "description": "Coordinate employee lifecycle milestones, manage benefits administration, and ensure labor regulation compliance."
    },

    # --- HEALTHCARE ---
    {
        "title": "Healthcare Data Scientist & Analyst",
        "company": "BioGenix Health",
        "category": "HEALTHCARE",
        "loc": ("Boston", "Massachusetts", "United States"),
        "salary_range": "$130,000 - $165,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "EMR/EHR, Python, Clinical Data, Biostatistics, HIPAA, SQL, Predictive Modeling",
        "description": "Analyze clinical trial outcomes, patient readmission factors, and develop healthcare quality metrics."
    },
    {
        "title": "Hospital Operations & Quality Manager",
        "company": "Apollo Multi-Specialty",
        "category": "HEALTHCARE",
        "loc": ("Chennai", "Tamil Nadu", "India"),
        "salary_range": "₹10,00,000 - ₹16,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Healthcare Administration, NABH Standards, Patient Safety, Clinical Workflows, Hospital Management",
        "description": "Streamline emergency care response times, lead accreditation compliance, and oversee patient service satisfaction."
    },

    # --- ENGINEERING (MECHANICAL / HARDWARE / CIVIL) ---
    {
        "title": "Robotics & Automation Systems Engineer",
        "company": "Kuka Automations",
        "category": "ENGINEERING",
        "loc": ("Munich", "Bavaria", "Germany"),
        "salary_range": "€80,000 - €105,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "CAD, SolidWorks, MATLAB, Robotics, PLC Programming, C++, Mechatronics, Prototyping",
        "description": "Develop autonomous robotic arms for automotive assembly lines, program PLC logic, and conduct rigorous stress simulations."
    },
    {
        "title": "Mechanical Design & Simulation Engineer",
        "company": "Tata Technologies",
        "category": "ENGINEERING",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹11,00,000 - ₹17,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "CATIA, ANSYS, FEA, Mechanical Design, GD&T, Thermal Analysis, Prototyping",
        "description": "Perform structural and thermal FEA simulations on chassis components, ensuring weight reduction and crash safety."
    },

    # --- BUSINESS-DEVELOPMENT & SALES ---
    {
        "title": "Enterprise Strategic Partnerships Director",
        "company": "SaaSMatrix Cloud",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$145,000 - $185,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "B2B Sales, Contract Negotiation, Strategic Alliances, Revenue Growth, CRM, Salesforce",
        "description": "Build high-impact strategic reseller channels and close million-dollar enterprise technology agreements."
    },
    {
        "title": "Regional Sales & Account Executive",
        "company": "GlobalTrade Connect",
        "category": "SALES",
        "loc": ("Singapore", "Central", "Singapore"),
        "salary_range": "S$90,000 - S$125,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "B2B SaaS Sales, Pipeline Management, Cold Outreach, Client Presentations, Negotiation",
        "description": "Expand market penetration across Southeast Asia, achieve quarterly revenue quotas, and manage senior stakeholder relationships."
    },
    {
        "title": "Inside Sales Specialist (FinTech)",
        "company": "RazorPay Partner Group",
        "category": "SALES",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹8,00,000 - ₹14,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior (1-3 yrs)",
        "required_skills": "Lead Qualification, Cold Calling, CRM, Presentation Skills, Objection Handling, Product Demo",
        "description": "Demonstrate modern payment gateway solutions to SME founders and exceed monthly qualified pipeline targets."
    },

    # --- DIGITAL-MEDIA ---
    {
        "title": "Head of Growth & Digital Marketing",
        "company": "ViralForge Agency",
        "category": "DIGITAL-MEDIA",
        "loc": ("Los Angeles", "California", "United States"),
        "salary_range": "$120,000 - $155,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "SEO, Performance Marketing, Google Ads, Meta Ads, Growth Hacking, Google Analytics, Copywriting",
        "description": "Direct multimillion-dollar advertising budgets, manage creative production, and scale customer acquisition by 180%."
    },
    {
        "title": "Content Strategy & SEO Specialist",
        "company": "BrandPulse Media",
        "category": "DIGITAL-MEDIA",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹9,00,000 - ₹15,00,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (2-4 yrs)",
        "required_skills": "Content Marketing, SEO, Keyword Research, Copywriting, Google Search Console, Social Media",
        "description": "Grow organic inbound web traffic through data-driven editorial calendars, technical SEO audits, and thought-leadership pieces."
    },

    # --- TEACHER / EDUCATION ---
    {
        "title": "Computer Science & AI Educator / Instructor",
        "company": "NextGen STEM Academy",
        "category": "TEACHER",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$80,000 - $105,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Python, Curriculum Development, Lesson Planning, Computer Science, Mentorship, Assessment",
        "description": "Deliver interactive coding masterclasses in Python and algorithms, mentor capstone student teams, and craft curriculum."
    },
    {
        "title": "Senior Mathematics & Data Lecturer",
        "company": "Imperial Scholars Foundation",
        "category": "TEACHER",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£45,000 - £60,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Pedagogy, Statistics, Calculus, Student Guidance, Online Teaching, Exam Preparation",
        "description": "Instruct undergraduate students in probability and discrete mathematics, creating engaging digital learning modules."
    },

    # --- CONSULTANT ---
    {
        "title": "Strategy & Digital Transformation Consultant",
        "company": "McKinsey Digital Advisory",
        "category": "CONSULTANT",
        "loc": ("Dubai", "Dubai", "United Arab Emirates"),
        "salary_range": "AED 280,000 - AED 380,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Management Consulting, Digital Strategy, Process Optimization, Financial Analysis, Executive Presentation",
        "description": "Advise C-level executives in the MENA region on digital modernization, cloud adoption, and operational reorganization."
    },

    # --- CONSTRUCTION ---
    {
        "title": "BIM Specialist & Construction Project Manager",
        "company": "Skanska Engineering Group",
        "category": "CONSTRUCTION",
        "loc": ("Sydney", "New South Wales", "Australia"),
        "salary_range": "A$110,000 - A$145,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "AutoCAD, BIM, Revit, Project Scheduling, OSHA Safety, Budget Estimation, Site Supervision",
        "description": "Coordinate multidimensional building information models (BIM) for commercial skyscraper construction."
    },

    # --- ADVOCATE / LEGAL ---
    {
        "title": "Corporate & Tech IP Legal Counsel",
        "company": "Lexis Legal Advisory",
        "category": "ADVOCATE",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹16,00,000 - ₹25,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Contract Drafting, Intellectual Property, Corporate Compliance, Dispute Resolution, Regulatory Law",
        "description": "Draft software licensing contracts, oversee patent filings, and protect corporate intellectual property assets."
    },

    # --- AVIATION ---
    {
        "title": "Avionics Systems & Flight Safety Specialist",
        "company": "SkyWings Aerospace",
        "category": "AVIATION",
        "loc": ("Dubai", "Dubai", "United Arab Emirates"),
        "salary_range": "AED 240,000 - AED 320,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Avionics, Aircraft Maintenance, FAA/EASA Regulations, Flight Operations, Safety Management Systems",
        "description": "Oversee diagnostic calibration of aircraft navigation systems and ensure total adherence to aviation safety protocols."
    },

    # --- CHEF ---
    {
        "title": "Executive Sous Chef",
        "company": "Grand Horizon Luxury Resort",
        "category": "CHEF",
        "loc": ("Paris", "Île-de-France", "France"),
        "salary_range": "€50,000 - €68,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Culinary Arts, Menu Planning, HACCP, Food Safety, Kitchen Staff Management, Fine Dining",
        "description": "Lead kitchen Brigade de Cuisine for Michelin-starred restaurant, design seasonal menus, and control food cost ratios."
    },

    # --- FITNESS ---
    {
        "title": "Elite Performance & Wellness Coach",
        "company": "Pulse Athletic Club",
        "category": "FITNESS",
        "loc": ("Melbourne", "Victoria", "Australia"),
        "salary_range": "A$75,000 - A$95,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Kinesiology, Strength & Conditioning, Nutrition, Injury Prevention, CPR/AED, Client Motivation",
        "description": "Design scientific training programs for competitive athletes and executives, monitoring biometric progress."
    },

    # --- APPAREL ---
    {
        "title": "Sustainable Fashion & Apparel Designer",
        "company": "EcoLoom Atelier",
        "category": "APPAREL",
        "loc": ("Milan / London", "Greater London", "United Kingdom"),
        "salary_range": "£50,000 - £68,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Garment Design, Textile Sourcing, Adobe Illustrator, Pattern Making, Sustainable Fashion, Trend Forecasting",
        "description": "Develop ready-to-wear seasonal apparel collections utilizing circular and organic textiles."
    },

    # --- AGRICULTURE ---
    {
        "title": "Precision Agronomy & Smart Farming Lead",
        "company": "AgriTech Innovations",
        "category": "AGRICULTURE",
        "loc": ("Chicago / Des Moines", "Illinois", "United States"),
        "salary_range": "$95,000 - $125,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Soil Science, Crop Scouting, GIS, Precision Farming, Irrigation Management, Drone Sensing",
        "description": "Implement satellite and IoT sensor arrays to optimize soil nutrient levels and boost crop yields by 25%."
    }
]

def seed_database():
    """Initializes tables and seeds initial worldwide job entries."""
    from database.db import init_db
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM jobs")
    row = cursor.fetchone()
    current_count = row["cnt"] if row else 0

    if current_count < 20:
        print(f"Seeding jobs... (currently {current_count})")
        for job in SAMPLE_JOBS:
            city, state, country = job["loc"]
            coords = WORLD_CITIES.get((city, state, country), (20.0, 0.0))
            insert_job(
                title=job["title"],
                company=job["company"],
                category=job["category"],
                city=city,
                state=state,
                country=country,
                lat=coords[0],
                lon=coords[1],
                salary_range=job["salary_range"],
                job_type=job["job_type"],
                experience_required=job["experience_required"],
                required_skills=job["required_skills"],
                description=job["description"],
                source="HireLens Global Network"
            )
        print(f"Seeded {len(SAMPLE_JOBS)} high-quality global job listings.")
    else:
        print(f"Database already contains {current_count} jobs.")
    conn.close()

if __name__ == "__main__":
    seed_database()
