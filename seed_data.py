"""
HireLens AI - Comprehensive Global Jobs Database Seeder
Populates 140+ diverse worldwide job opportunities across ALL 24 categories from Kaggle Resume dataset.
Covers cities and states across North America, India, Europe, UK, Asia, Australia, and Middle East.
"""
try:
    from database.db import get_connection, insert_job
except ModuleNotFoundError:
    from db import get_connection, insert_job

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
    ("Atlanta", "Georgia", "United States"): (33.7490, -84.3880),
    ("Des Moines", "Iowa", "United States"): (41.5868, -93.6250),
    # India
    ("Bengaluru", "Karnataka", "India"): (12.9716, 77.5946),
    ("Mumbai", "Maharashtra", "India"): (19.0760, 72.8777),
    ("Hyderabad", "Telangana", "India"): (17.3850, 78.4867),
    ("Pune", "Maharashtra", "India"): (18.5204, 73.8567),
    ("New Delhi", "Delhi", "India"): (28.6139, 77.2090),
    ("Chennai", "Tamil Nadu", "India"): (13.0827, 80.2707),
    ("Gurugram", "Haryana", "India"): (28.4595, 77.0266),
    ("Noida", "Uttar Pradesh", "India"): (28.5355, 77.3910),
    ("Kolkata", "West Bengal", "India"): (22.5726, 88.3639),
    # United Kingdom
    ("London", "Greater London", "United Kingdom"): (51.5074, -0.1278),
    ("Manchester", "Greater Manchester", "United Kingdom"): (53.4808, -2.2426),
    ("Edinburgh", "Scotland", "United Kingdom"): (55.9533, -3.1883),
    # Europe
    ("Berlin", "Berlin", "Germany"): (52.5200, 13.4050),
    ("Munich", "Bavaria", "Germany"): (48.1351, 11.5820),
    ("Frankfurt", "Hesse", "Germany"): (50.1109, 8.6821),
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

ALL_FIELD_JOBS = [
    # ==================== 1. ACCOUNTANT ====================
    {
        "title": "Senior Corporate Accountant",
        "company": "Vanguard Financial Partners",
        "category": "ACCOUNTANT",
        "loc": ("Chicago", "Illinois", "United States"),
        "salary_range": "$90,000 - $115,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "GAAP, General Ledger, Financial Statements, Reconciliation, QuickBooks, ERP, Attention to Detail, Auditing",
        "description": "Oversee general ledger operations, manage monthly close cycles, prepare variance analyses, and coordinate audit requests."
    },
    {
        "title": "Tax Compliance & Audit Specialist",
        "company": "KPMG Advisory India",
        "category": "ACCOUNTANT",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹14,00,000 - ₹20,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Direct & Indirect Tax, GST, Income Tax, Tally, Auditing, Statutory Compliance, Regulatory Compliance, Analytical Skills",
        "description": "Lead statutory tax assessments, prepare corporate tax filings, and advise corporate clients on indirect tax optimizations."
    },
    {
        "title": "Staff Accountant & Financial Analyst",
        "company": "MapleLeaf Financial",
        "category": "ACCOUNTANT",
        "loc": ("Toronto", "Ontario", "Canada"),
        "salary_range": "C$75,000 - C$95,000",
        "job_type": "Hybrid",
        "experience_required": "Junior (1-3 yrs)",
        "required_skills": "IFRS, Accounts Payable, Accounts Receivable, Excel, Reconciliation, Organization, Communication",
        "description": "Reconcile balance sheet accounts, streamline invoice tracking, and prepare monthly cash flow schedules."
    },
    {
        "title": "Forensic Accountant & Fraud Investigator",
        "company": "Grant Thornton UK",
        "category": "ACCOUNTANT",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£65,000 - £85,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Forensic Accounting, Auditing, Internal Audit, Financial Investigation, Critical Thinking, Attention to Detail",
        "description": "Investigate financial anomalies, reconstruct accounting records, and prepare expert witness documentation for dispute cases."
    },
    {
        "title": "Cost & Management Accountant",
        "company": "Tata Motors Manufacturing",
        "category": "ACCOUNTANT",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹12,00,000 - ₹18,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Cost Accounting, Variance Analysis, Budgeting, ERP, SAP, Inventory Control, Problem Solving",
        "description": "Analyze manufacturing overhead costs, set bill-of-materials standard costs, and drive factory cost optimization."
    },

    # ==================== 2. ADVOCATE ====================
    {
        "title": "Corporate Legal Counsel & M&A Specialist",
        "company": "Lexis Advisory Partners",
        "category": "ADVOCATE",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$160,000 - $210,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Corporate Law, Due Diligence, M&A, Contract Negotiation, Legal Drafting, Regulatory Compliance, Negotiation",
        "description": "Structure mergers and acquisitions, draft commercial purchase agreements, and ensure multi-jurisdictional compliance."
    },
    {
        "title": "Intellectual Property & Tech Patent Attorney",
        "company": "Silicon Valley Law Group",
        "category": "ADVOCATE",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$175,000 - $230,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (5+ yrs)",
        "required_skills": "Intellectual Property, Patents, Trademarks, Tech Licensing, Legal Research, Critical Thinking, Persuasion",
        "description": "Advise high-growth AI and biotechnology companies on patent strategy, IP portfolios, and licensing disputes."
    },
    {
        "title": "Commercial Litigation & Dispute Advocate",
        "company": "Supreme Chambers",
        "category": "ADVOCATE",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹16,00,000 - ₹26,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Litigation, Dispute Resolution, Arbitration, Legal Research, Public Speaking, Argumentation, Ethics",
        "description": "Represent corporate clients before High Courts and arbitration tribunals in breach of contract and commercial matters."
    },
    {
        "title": "Commercial Contracts Specialist",
        "company": "Allen & Overy LLP",
        "category": "ADVOCATE",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£85,000 - £115,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Contract Management, Legal Drafting, Risk Assessment, Cross-Border Law, Negotiation, Attention to Detail",
        "description": "Review and negotiate enterprise vendor, SaaS licensing, and procurement agreements across European markets."
    },
    {
        "title": "Regulatory & FinTech Compliance Legal Officer",
        "company": "PayGlobal Solutions",
        "category": "ADVOCATE",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹15,00,000 - ₹22,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Regulatory Compliance, RBI Regulations, Privacy Laws, Due Diligence, Communication, Problem Solving",
        "description": "Interface with financial regulatory authorities, audit cross-border transaction flows, and maintain compliance standards."
    },

    # ==================== 3. AGRICULTURE ====================
    {
        "title": "Precision Agronomy & Smart Farming Lead",
        "company": "AgriTech Innovations",
        "category": "AGRICULTURE",
        "loc": ("Des Moines", "Iowa", "United States"),
        "salary_range": "$95,000 - $125,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Precision Agriculture, Soil Science, Crop Management, GIS, Drone Sensing, Data Analysis, Problem Solving",
        "description": "Deploy satellite imagery and IoT soil sensors to formulate variable-rate fertilization programs, increasing yields by 25%."
    },
    {
        "title": "Sustainable Farming Operations Manager",
        "company": "GreenFields Agrobusiness",
        "category": "AGRICULTURE",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹10,00,000 - ₹16,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Sustainable Farming, Organic Agriculture, Irrigation Management, Team Leadership, Supply Chain, Resource Allocation",
        "description": "Direct 1,200 acres of regenerative crop cultivation, manage drip-irrigation networks, and coordinate farm workers."
    },
    {
        "title": "Vertical Farming Systems Specialist",
        "company": "UrbanCrop Technologies",
        "category": "AGRICULTURE",
        "loc": ("Singapore", "Central", "Singapore"),
        "salary_range": "S$80,000 - S$105,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-4 yrs)",
        "required_skills": "Hydroponics, CEA, Plant Physiology, Environmental Controls, Nutrient Management, Research",
        "description": "Optimize LED spectra and hydroponic nutrient solutions for commercial vertical farm facilities in urban Singapore."
    },
    {
        "title": "Agribusiness Supply Chain & Procurement Analyst",
        "company": "Bunge Global Ag",
        "category": "AGRICULTURE",
        "loc": ("Chicago", "Illinois", "United States"),
        "salary_range": "$85,000 - $110,000",
        "job_type": "Hybrid",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Commodity Trading, Agribusiness, Supply Chain Management, Logistics, Market Research, Forecasting",
        "description": "Forecast grain demand trends, negotiate regional farmer contracts, and streamline logistics to processing facilities."
    },
    {
        "title": "Agricultural Pest & Crop Protection Specialist",
        "company": "BioFlora Australia",
        "category": "AGRICULTURE",
        "loc": ("Sydney", "New South Wales", "Australia"),
        "salary_range": "A$90,000 - A$115,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Pest Control, Agronomy, Entomology, Soil Health, Environmental Safety, Technical Reporting",
        "description": "Design integrated pest management protocols, minimizing chemical usage and enhancing beneficial insect populations."
    },

    # ==================== 4. APPAREL ====================
    {
        "title": "Sustainable Fashion & Apparel Designer",
        "company": "EcoLoom Atelier",
        "category": "APPAREL",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£50,000 - £70,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Fashion Design, Textiles, Adobe Illustrator, Pattern Making, Sourcing, Trend Forecasting, Creative Vision",
        "description": "Develop ready-to-wear seasonal apparel collections utilizing circular and organic textiles with zero-waste patterns."
    },
    {
        "title": "Apparel Sourcing & Production Manager",
        "company": "Inditex Global Brand",
        "category": "APPAREL",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$95,000 - $125,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Garment Manufacturing, Vendor Management, Quality Control, Supply Chain, Negotiation, Costing",
        "description": "Oversee offshore garment manufacturing runs, audit factory compliance, and ensure target FOB costs."
    },
    {
        "title": "Senior Textile Technologist & Quality Analyst",
        "company": "Arvind Mills",
        "category": "APPAREL",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹11,00,000 - ₹17,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Textile Science, Fabric Testing, Dyeing & Finishing, Quality Assurance, Material Specifications, Attention to Detail",
        "description": "Supervise physical and chemical fabric testing, ensure colorfastness and tensile strength against international standards."
    },
    {
        "title": "Digital 3D Fashion Designer (Clo3D / Browzwear)",
        "company": "MetaStyle Virtual Studio",
        "category": "APPAREL",
        "loc": ("Los Angeles", "California", "United States"),
        "salary_range": "$85,000 - $115,000",
        "job_type": "Remote",
        "experience_required": "Junior-Mid (2-4 yrs)",
        "required_skills": "Clo3D, 3D Garment Simulation, Adobe Creative Suite, Digital Prototyping, Texturing, Creativity",
        "description": "Create photorealistic 3D digital garment samples in Clo3D, reducing physical sampling rounds by 70%."
    },
    {
        "title": "Technical Apparel Pattern Maker & Grader",
        "company": "Lululemon Athletica",
        "category": "APPAREL",
        "loc": ("Vancouver", "British Columbia", "Canada"),
        "salary_range": "C$75,000 - C$98,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Pattern Drafting, Gerber Accumark, Fit Analysis, Activewear, Grading, Precision, Collaboration",
        "description": "Engineer performance activewear patterns, conduct live fit sessions with athletes, and refine size grading specifications."
    },

    # ==================== 5. ARTS ====================
    {
        "title": "Lead Concept Artist & Digital Illustrator",
        "company": "Riot Games & Media",
        "category": "ARTS",
        "loc": ("Los Angeles", "California", "United States"),
        "salary_range": "$110,000 - $145,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Concept Art, Digital Painting, Photoshop, Visual Storytelling, Character Design, Creative Direction, Anatomic Drawing",
        "description": "Design cinematic environment concept art and character stylesheets for next-generation interactive titles."
    },
    {
        "title": "Contemporary Art Curator & Exhibition Director",
        "company": "Tate Modern Arts",
        "category": "ARTS",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£55,000 - £75,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Art Curation, Exhibition Planning, Art History, Critical Writing, Artist Relations, Budgeting, Public Speaking",
        "description": "Curate international contemporary art retrospectives, manage catalog publications, and liaise with collectors."
    },
    {
        "title": "Creative Art Director & Brand Visualist",
        "company": "Ogilvy Creative Collective",
        "category": "ARTS",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹15,00,000 - ₹24,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Creative Direction, Visual Design, Typography, Campaign Strategy, Brand Storytelling, Team Leadership",
        "description": "Direct cross-media advertising visuals, mentor art directors, and lead visual execution for global brands."
    },
    {
        "title": "Fine Arts Conservator & Restoration Specialist",
        "company": "Louvre Heritage Labs",
        "category": "ARTS",
        "loc": ("Paris", "Île-de-France", "France"),
        "salary_range": "€48,000 - €65,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Art Restoration, Material Analysis, Pigment Chemistry, Documentation, Patience, Attention to Detail",
        "description": "Perform meticulous cleaning and structural stabilization of classical oil paintings using non-invasive techniques."
    },
    {
        "title": "Digital Matte Painter & Environment Artist",
        "company": "Industrial Light & Magic (ILM)",
        "category": "ARTS",
        "loc": ("Vancouver", "British Columbia", "Canada"),
        "salary_range": "C$90,000 - C$120,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Matte Painting, Nuke, Maya, Photoshop, Photorealism, Lighting, Compositing",
        "description": "Create photorealistic background vistas and 2.5D projections for major Hollywood motion pictures."
    },

    # ==================== 6. AUTOMOBILE ====================
    {
        "title": "EV Battery Systems & Powertrain Engineer",
        "company": "Tesla Motors",
        "category": "AUTOMOBILE",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$135,000 - $175,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Automotive Engineering, EV Powertrain, Battery Management Systems, Thermal Analysis, MATLAB, Simulink, CAD",
        "description": "Design high-voltage lithium-ion pack enclosures, model thermal dissipation, and optimize battery pack efficiency."
    },
    {
        "title": "Automotive Diagnostics & Calibration Specialist",
        "company": "Robert Bosch Mobility",
        "category": "AUTOMOBILE",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹12,00,000 - ₹19,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "ECU Calibration, CAN Bus, OBD-II, Diagnostics, Embedded C, Vehicle Testing, Troubleshooting",
        "description": "Calibrate engine management ECUs for BS-VI emission standards, run chassis dyno trials, and resolve driveability faults."
    },
    {
        "title": "Vehicle Dynamics & NVH Simulation Specialist",
        "company": "BMW Group",
        "category": "AUTOMOBILE",
        "loc": ("Munich", "Bavaria", "Germany"),
        "salary_range": "€75,000 - €100,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "NVH Analysis, Vehicle Dynamics, Adams, ANSYS, Suspension Design, Prototyping, Problem Solving",
        "description": "Analyze acoustic and vibrational characteristics of premium chassis architectures to eliminate road cabin noise."
    },
    {
        "title": "Automotive Safety & Crash Simulation Engineer",
        "company": "Tata Motors R&D",
        "category": "AUTOMOBILE",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹13,00,000 - ₹20,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Crash Simulation, LS-DYNA, Non-Linear FEA, Structural Analysis, Safety Standards, Automotive Design",
        "description": "Conduct virtual frontal and side impact crash simulations to achieve 5-star Bharat NCAP vehicle safety ratings."
    },
    {
        "title": "Autonomous Driving Systems Integrator",
        "company": "Waymo LLC",
        "category": "AUTOMOBILE",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$150,000 - $195,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Autonomous Vehicles, LiDAR, Sensor Fusion, ROS, Python, C++, Linux, Safety Testing",
        "description": "Integrate perception sensor suites into production robotaxi platforms and validate sensor calibration stability."
    },

    # ==================== 7. AVIATION ====================
    {
        "title": "Flight Operations & Crew Scheduling Lead",
        "company": "Emirates Airlines",
        "category": "AVIATION",
        "loc": ("Dubai", "Dubai", "United Arab Emirates"),
        "salary_range": "AED 240,000 - AED 310,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Flight Operations, Crew Resource Management, FAA/EASA Regulations, Dispatch, Aviation Safety, Decisiveness",
        "description": "Orchestrate global flight routing schedules, monitor en-route weather disturbances, and enforce FAA dispatch protocols."
    },
    {
        "title": "Avionics Systems Maintenance Specialist",
        "company": "Boeing Global Services",
        "category": "AVIATION",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$105,000 - $135,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Avionics, Aircraft Maintenance, FAA Regulations, Troubleshooting, Wiring Schematics, Quality Control",
        "description": "Inspect and calibrate fly-by-wire flight control computers, radar transponders, and navigational sensor arrays."
    },
    {
        "title": "Aircraft Fleet Reliability & Maintenance Analyst",
        "company": "Delta Air Lines",
        "category": "AVIATION",
        "loc": ("Atlanta", "Georgia", "United States"),
        "salary_range": "$90,000 - $120,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Aircraft Maintenance, Predictive Maintenance, Reliability Engineering, SQL, Safety Management Systems",
        "description": "Analyze engine telemetry data to predict component wear cycles and prevent unscheduled fleet groundings."
    },
    {
        "title": "Air Traffic Safety & Navigation Coordinator",
        "company": "Airports Authority of India",
        "category": "AVIATION",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹12,00,000 - ₹18,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Air Traffic Control, Navigation Systems, Radar Operations, Stress Management, Clear Communication, ICAO Standards",
        "description": "Manage terminal airspace separation matrices, coordinate emergency vectors, and audit navigational aids."
    },
    {
        "title": "Aerospace Propulsion Systems Engineer",
        "company": "Rolls-Royce Aerospace",
        "category": "AVIATION",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£75,000 - £100,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Gas Turbine Propulsion, Aerodynamics, Thermodynamics, MATLAB, CFD, Aviation Safety",
        "description": "Design low-emission combustor liners for commercial jet turbofans, running fluid-thermal dynamic simulations."
    },

    # ==================== 8. BANKING ====================
    {
        "title": "Commercial Credit Risk Underwriter",
        "company": "HDFC Bank Corporate",
        "category": "BANKING",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹15,00,000 - ₹24,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Credit Analysis, Financial Statements, Risk Assessment, Corporate Loans, Due Diligence, Decision Making",
        "description": "Appraise multi-million dollar corporate debt facilities, evaluate cash flow coverage ratios, and structure debt covenants."
    },
    {
        "title": "Private Wealth Portfolio Advisor",
        "company": "UBS Switzerland",
        "category": "BANKING",
        "loc": ("Zurich", "Zurich", "Switzerland"),
        "salary_range": "CHF 130,000 - CHF 170,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Wealth Management, Portfolio Management, Asset Allocation, Relationship Building, Trust, Financial Planning",
        "description": "Manage customized multi-asset investment portfolios for high-net-worth families with strict fiduciary integrity."
    },
    {
        "title": "Retail Banking Operations Branch Manager",
        "company": "Barclays Bank UK",
        "category": "BANKING",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£60,000 - £80,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Retail Banking, Branch Operations, Customer Relationship Management, Team Leadership, KYC, Compliance",
        "description": "Direct branch banking operations, mentor financial services staff, and ensure adherence to FCA conduct rules."
    },
    {
        "title": "FinTech AML & Financial Crime Specialist",
        "company": "Revolut FinTech",
        "category": "BANKING",
        "loc": ("Dublin", "Leinster", "Ireland"),
        "salary_range": "€65,000 - €85,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "AML, KYC, Sanctions Screening, Transaction Monitoring, Investigation, Critical Thinking, Regulatory Compliance",
        "description": "Investigate suspicious transaction alerts, file Suspicious Activity Reports (SARs), and update AML risk typologies."
    },
    {
        "title": "Treasury & Liquidity Risk Manager",
        "company": "DBS Bank",
        "category": "BANKING",
        "loc": ("Singapore", "Central", "Singapore"),
        "salary_range": "S$110,000 - S$145,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Treasury Management, Liquidity Risk, Basel III, Capital Markets, Cash Management, Financial Modeling",
        "description": "Manage institutional liquidity coverage ratios (LCR) and execute money-market funding strategies."
    },

    # ==================== 9. BPO ====================
    {
        "title": "Senior Customer Experience Lead",
        "company": "Concentrix Global",
        "category": "BPO",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹8,00,000 - ₹13,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Customer Support, CRM, Active Listening, Team Leadership, Conflict Resolution, Empathy, Communication",
        "description": "Lead a team of 25 customer service representatives handling Tier-2 escalation tickets for global tech clients."
    },
    {
        "title": "International Inbound Process Specialist",
        "company": "Teleperformance India",
        "category": "BPO",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹6,00,000 - ₹9,50,000",
        "job_type": "Full-time",
        "experience_required": "Junior (1-3 yrs)",
        "required_skills": "Telecalling, Inbound Support, Customer Service, Verbal Communication, Problem Solving, Adaptability",
        "description": "Provide high-empathy customer support for North American telecommunication subscribers, meeting 95%+ CSAT targets."
    },
    {
        "title": "BPO Call Quality & SLA Assurance Manager",
        "company": "Genpact Enterprise",
        "category": "BPO",
        "loc": ("Gurugram", "Haryana", "India"),
        "salary_range": "₹11,00,000 - ₹16,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Quality Assurance, KPI Management, SLA Tracking, Coaching, Root Cause Analysis, Auditing",
        "description": "Audit voice and chat customer interactions, calibrate scoring rubrics, and deliver targeted coaching to underperforming squads."
    },
    {
        "title": "Customer Escalations & Retention Executive",
        "company": "WNS Global Services",
        "category": "BPO",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹7,00,000 - ₹11,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (1-4 yrs)",
        "required_skills": "Conflict De-escalation, Customer Retention, Negotiation, Patience, CRM, Problem Solving",
        "description": "Resolve critical high-priority customer complaints and implement retention offers to salvage at-risk accounts."
    },
    {
        "title": "Workforce Management (WFM) Scheduling Analyst",
        "company": "Cognizant BPO",
        "category": "BPO",
        "loc": ("Hyderabad", "Telangana", "India"),
        "salary_range": "₹9,00,000 - ₹14,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Workforce Planning, Erlang C, Capacity Modeling, Scheduling, Data Analysis, Excel",
        "description": "Model call volume arrival patterns using Erlang C algorithms to build optimal multi-shift agent rosters."
    },

    # ==================== 10. BUSINESS-DEVELOPMENT ====================
    {
        "title": "Enterprise Strategic Partnerships Director",
        "company": "Salesforce Cloud",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$160,000 - $210,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Strategic Partnerships, B2B Sales, Contract Negotiation, Revenue Growth, CRM, Strategic Planning",
        "description": "Build high-impact strategic channel partnerships, co-sell programs, and negotiate multi-year distribution alliances."
    },
    {
        "title": "Global Business Development Manager",
        "company": "Amazon Web Services (AWS)",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$145,000 - $185,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Cloud Solutions, Business Development, Account Management, Pipeline Management, Executive Communication",
        "description": "Drive cloud migration adoption among enterprise conglomerates, formulating customized business transformation proposals."
    },
    {
        "title": "B2B Strategic Growth Lead",
        "company": "Swiggy B2B Commerce",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹18,00,000 - ₹28,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Lead Generation, B2B Sales, Market Expansion, Negotiation, Data-Driven Decision Making, Networking",
        "description": "Onboard national restaurant chains and FMCG suppliers onto the enterprise bulk-procurement portal."
    },
    {
        "title": "Corporate Strategy & Technology Alliances Manager",
        "company": "Stripe Global",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£90,000 - £120,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "FinTech, Strategic Alliances, Market Research, Revenue Strategy, Stakeholder Management",
        "description": "Develop strategic partnerships with European payment processors, merchant aggregators, and banking sponsors."
    },
    {
        "title": "Emerging Market Expansion Specialist",
        "company": "Grab SuperApp",
        "category": "BUSINESS-DEVELOPMENT",
        "loc": ("Singapore", "Central", "Singapore"),
        "salary_range": "S$95,000 - S$130,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Market Entry, Business Development, Competitive Analysis, Cross-Cultural Communication, Negotiation",
        "description": "Conduct feasibility studies and negotiate regulatory agreements to expand on-demand services across Southeast Asian cities."
    },

    # ==================== 11. CHEF ====================
    {
        "title": "Executive Sous Chef",
        "company": "Grand Horizon Luxury Resort",
        "category": "CHEF",
        "loc": ("Paris", "Île-de-France", "France"),
        "salary_range": "€55,000 - €75,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Culinary Arts, Menu Planning, HACCP, Food Safety, Kitchen Management, Fine Dining, Team Leadership",
        "description": "Lead the kitchen Brigade de Cuisine for a Michelin-starred dining room, craft seasonal menus, and control food cost percentages."
    },
    {
        "title": "Head Pastry Chef & Chocolatier",
        "company": "L'Artisan Bakery Atelier",
        "category": "CHEF",
        "loc": ("Zurich", "Zurich", "Switzerland"),
        "salary_range": "CHF 70,000 - CHF 92,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Pastry Arts, Chocolate Tempering, Recipe Formulation, Food Safety, Creativity, Attention to Detail",
        "description": "Create artisanal viennoiserie, gourmet entremets, and bespoke chocolate showpieces for luxury retail boutiques."
    },
    {
        "title": "Executive Master Chef - Indian Fine Dining",
        "company": "Taj Luxury Hotels",
        "category": "CHEF",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹16,00,000 - ₹25,00,000",
        "job_type": "Full-time",
        "experience_required": "Senior (6+ yrs)",
        "required_skills": "Culinary Leadership, Traditional Indian Gastronomy, Kitchen Operations, Staff Training, Cost Control",
        "description": "Direct culinary vision across 3 flagship property restaurants, standardizing authentic royal recipes and presentation."
    },
    {
        "title": "Farm-to-Table Head Chef",
        "company": "Greenwood Seasonal Kitchen",
        "category": "CHEF",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$85,000 - $110,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Sustainable Cooking, Local Sourcing, Menu Planning, Inventory Control, Creativity, Stress Management",
        "description": "Curate hyper-seasonal weekly tasting menus utilizing produce sourced exclusively from Northern California organic farms."
    },
    {
        "title": "Executive Banquet & Catering Chef",
        "company": "Marriott International",
        "category": "CHEF",
        "loc": ("Dubai", "Dubai", "United Arab Emirates"),
        "salary_range": "AED 180,000 - AED 240,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Banquet Operations, High-Volume Catering, HACCP, Event Logistics, Team Leadership, Multi-Cuisine",
        "description": "Coordinate mass culinary execution for high-profile diplomatic banquets and galas hosting up to 2,000 guests."
    },

    # ==================== 12. CONSTRUCTION ====================
    {
        "title": "BIM Specialist & Construction Project Manager",
        "company": "Skanska Engineering Group",
        "category": "CONSTRUCTION",
        "loc": ("Sydney", "New South Wales", "Australia"),
        "salary_range": "A$115,000 - A$150,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "BIM, AutoCAD, Revit, Project Scheduling, OSHA Safety, Budgeting, Site Supervision, Conflict Resolution",
        "description": "Coordinate multidimensional building information models (BIM) for commercial high-rise construction, resolving clashes."
    },
    {
        "title": "Civil Site Supervision & Execution Engineer",
        "company": "Larsen & Toubro (L&T)",
        "category": "CONSTRUCTION",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹11,00,000 - ₹17,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Site Supervision, RCC Construction, Quality Control, Contractor Management, Blueprint Reading, Safety Culture",
        "description": "Direct on-site pouring of reinforced concrete, inspect reinforcement steel cages, and ensure adherence to IS codes."
    },
    {
        "title": "Senior Structural Design & Engineering Lead",
        "company": "Arup Consulting Engineers",
        "category": "CONSTRUCTION",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£70,000 - £95,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Structural Engineering, Steel & Concrete Design, Eurocodes, ETABS, Finite Element Modeling, Problem Solving",
        "description": "Design structural steel superstructures and deep foundation pile groups for complex transit infrastructure hubs."
    },
    {
        "title": "Commercial Construction Estimator",
        "company": "Turner Construction",
        "category": "CONSTRUCTION",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$95,000 - $130,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Cost Estimation, Quantity Surveying, PlanSwift, Subcontractor Bidding, Value Engineering, Negotiation",
        "description": "Calculate comprehensive material takeoffs and labor estimates for multimillion-dollar commercial interior buildouts."
    },
    {
        "title": "OSHA Environmental Health & Safety (EHS) Director",
        "company": "Bechtel Infrastructure",
        "category": "CONSTRUCTION",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$100,000 - $135,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "OSHA Safety, EHS Compliance, Hazard Identification, Incident Investigation, Worker Safety Training, Leadership",
        "description": "Enforce zero-accident safety protocols across heavy highway construction projects, conducting weekly site safety audits."
    },

    # ==================== 13. CONSULTANT ====================
    {
        "title": "Strategy & Digital Transformation Consultant",
        "company": "McKinsey Digital Advisory",
        "category": "CONSULTANT",
        "loc": ("Dubai", "Dubai", "United Arab Emirates"),
        "salary_range": "AED 290,000 - AED 390,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Management Consulting, Digital Strategy, Process Optimization, Financial Analysis, Executive Presentation, Problem Solving",
        "description": "Advise C-level executives on digital modernization, cloud adoption, and operational reorganization across the GCC."
    },
    {
        "title": "Operations & Lean Six Sigma Consultant",
        "company": "Boston Consulting Group (BCG)",
        "category": "CONSULTANT",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$165,000 - $215,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Lean Six Sigma, Process Improvement, Supply Chain, Change Management, Data Analysis, Stakeholder Management",
        "description": "Lead manufacturing operational diagnostics, eliminating production bottlenecks and saving clients $20M+ annually."
    },
    {
        "title": "Business Strategy & Technology Associate",
        "company": "Bain & Company",
        "category": "CONSULTANT",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£80,000 - £110,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Market Sizing, Financial Modeling, Competitive Benchmarking, PowerPoint, Structured Problem Solving, Critical Thinking",
        "description": "Conduct commercial due diligence for private equity sponsors, modeling total addressable market and customer retention."
    },
    {
        "title": "Business Transformation & Process Consultant",
        "company": "Accenture Strategy India",
        "category": "CONSULTANT",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹18,00,000 - ₹28,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Business Process Modeling, ERP Advisory, Change Management, KPI Development, Stakeholder Communication",
        "description": "Guide multinational enterprises through SAP S/4HANA migrations, redesigning procurement and inventory processes."
    },
    {
        "title": "Financial Turnaround & Restructuring Consultant",
        "company": "Alvarez & Marsal",
        "category": "CONSULTANT",
        "loc": ("Chicago", "Illinois", "United States"),
        "salary_range": "$140,000 - $185,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Restructuring, Cash Flow Forecasting, Working Capital, Debt Advisory, Negotiation, Analytical Skills",
        "description": "Stabilize distressed middle-market companies, formulate 13-week cash forecasts, and negotiate creditor forbearance."
    },

    # ==================== 14. DESIGNER ====================
    {
        "title": "Lead UI/UX & Design Systems Architect",
        "company": "Aura Design Co",
        "category": "DESIGNER",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$130,000 - $165,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Figma, UI/UX, Design Systems, Typography, Wireframing, Prototyping, User Research, User Empathy",
        "description": "Establish multi-platform design systems with tokenized typography and color palettes, ensuring high accessibility (WCAG)."
    },
    {
        "title": "Senior Product Interaction Designer",
        "company": "Stripe Interactive",
        "category": "DESIGNER",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$140,000 - $180,000",
        "job_type": "Remote",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Interaction Design, Figma, Micro-Interactions, Usability Testing, Visual Design, HTML/CSS basics",
        "description": "Craft checkout interfaces and financial dashboards with silky micro-interactions that minimize cart abandonment."
    },
    {
        "title": "Mobile UI/UX Product Designer",
        "company": "Flipkart Internet",
        "category": "DESIGNER",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹16,00,000 - ₹25,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Mobile UX, Android Design Guidelines, Figma, User Journey Mapping, A/B Testing, Cross-Functional Collaboration",
        "description": "Redesign mobile grocery shopping flows for 100M+ active users, conducting in-person usability studies in Tier-2 Indian cities."
    },
    {
        "title": "Brand Visual & Graphic Design Lead",
        "company": "Studio Dumbar Branding",
        "category": "DESIGNER",
        "loc": ("Amsterdam", "North Holland", "Netherlands"),
        "salary_range": "€62,000 - €82,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Graphic Design, Adobe Photoshop, Illustrator, InDesign, Brand Identity, Motion Graphics, Creative Direction",
        "description": "Develop full-scale visual identity packages, packaging guidelines, and motion identities for European cultural brands."
    },
    {
        "title": "Senior UX Researcher & Usability Lead",
        "company": "Google LLC",
        "category": "DESIGNER",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$145,000 - $185,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "User Research, Usability Testing, Qualitative Analysis, Survey Design, Persona Development, Empathy, Presentation",
        "description": "Lead mixed-method user research studies to uncover customer mental models and guide strategic feature roadmaps."
    },

    # ==================== 15. DIGITAL-MEDIA ====================
    {
        "title": "Head of Performance Marketing & Growth",
        "company": "ViralForge Agency",
        "category": "DIGITAL-MEDIA",
        "loc": ("Los Angeles", "California", "United States"),
        "salary_range": "$125,000 - $160,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Performance Marketing, Google Ads, Meta Ads, Growth Hacking, Google Analytics, Copywriting, Data Analysis",
        "description": "Deploy multimillion-dollar paid advertising budgets, optimize blended CAC/LTV ratios, and scale e-commerce revenues."
    },
    {
        "title": "Technical SEO & Inbound Marketing Strategist",
        "company": "HubSpot",
        "category": "DIGITAL-MEDIA",
        "loc": ("Boston", "Massachusetts", "United States"),
        "salary_range": "$90,000 - $120,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "SEO, Technical SEO, Keyword Research, Content Strategy, Google Search Console, Ahrefs, Web Performance",
        "description": "Conduct deep technical site audits, optimize Core Web Vitals, and build topic cluster models driving organic search."
    },
    {
        "title": "Digital Content Producer & Video Director",
        "company": "Vox Media Collective",
        "category": "DIGITAL-MEDIA",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$80,000 - $105,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Video Editing, Premiere Pro, After Effects, Creative Storytelling, Scriptwriting, Audio Production, Social Video",
        "description": "Produce and edit short-form and documentary-style video content for YouTube and digital streaming platforms."
    },
    {
        "title": "Social Media & Community Engagement Director",
        "company": "ByteDance / TikTok UK",
        "category": "DIGITAL-MEDIA",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£60,000 - £80,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Social Media Marketing, Community Management, Trend Analysis, Copywriting, Influencer Partnerships, Brand Voice",
        "description": "Spearhead pan-European social media campaigns, engage with creator communities, and grow platform audience engagement."
    },
    {
        "title": "Organic Growth & Content Strategy Lead",
        "company": "Swiggy Brand Labs",
        "category": "DIGITAL-MEDIA",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹12,00,000 - ₹19,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Content Marketing, Copywriting, SEO, Social Media, Creative Storytelling, Analytics",
        "description": "Craft viral social media copywriting and content campaigns, elevating organic brand recall and consumer engagement."
    },

    # ==================== 16. ENGINEERING ====================
    {
        "title": "Robotics & Automation Systems Engineer",
        "company": "Kuka Automation Systems",
        "category": "ENGINEERING",
        "loc": ("Munich", "Bavaria", "Germany"),
        "salary_range": "€82,000 - €108,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Robotics, PLC Programming, C++, CAD, MATLAB, Mechatronics, Prototyping, Problem Solving",
        "description": "Program 6-axis industrial articulated robotic cells for precision assembly lines, tuning kinematic path accuracy."
    },
    {
        "title": "Mechanical Design & FEA Simulation Engineer",
        "company": "Tata Technologies",
        "category": "ENGINEERING",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹12,00,000 - ₹18,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "SolidWorks, CATIA, ANSYS, FEA, Mechanical Design, GD&T, Thermal Analysis, Prototyping",
        "description": "Execute structural finite element analyses on heavy machinery brackets, optimizing weight while ensuring fatigue life."
    },
    {
        "title": "Electrical Power Systems Design Engineer",
        "company": "Siemens Energy",
        "category": "ENGINEERING",
        "loc": ("Berlin", "Berlin", "Germany"),
        "salary_range": "€78,000 - €102,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Electrical Engineering, High Voltage, Power Distribution, Switchgear Design, Circuit Simulation, Quality Control",
        "description": "Design high-voltage substation switchgear packages and power transformer protection relays for grid interconnection."
    },
    {
        "title": "Embedded Hardware & Firmware Engineer",
        "company": "Apple Inc.",
        "category": "ENGINEERING",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$150,000 - $195,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Embedded C, PCB Design, Microcontrollers, ARM, I2C, SPI, Hardware Troubleshooting, Linux",
        "description": "Architect low-power sensor interface boards and real-time firmware drivers for next-generation hardware devices."
    },
    {
        "title": "Aerospace Thermal & Structural Dynamics Engineer",
        "company": "Lockheed Martin",
        "category": "ENGINEERING",
        "loc": ("Denver", "Colorado", "United States"),
        "salary_range": "$120,000 - $155,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Thermodynamics, Structural Analysis, Thermal Simulation, Cryogenics, MATLAB, Nastran, Quality Assurance",
        "description": "Perform cryogenic thermal modeling for satellite radiator surfaces subjected to orbital vacuum cycles."
    },

    # ==================== 17. FINANCE ====================
    {
        "title": "Senior Financial Analyst & Valuation Modeler",
        "company": "Apex Capital Management",
        "category": "FINANCE",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$140,000 - $175,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Financial Modeling, Valuation, DCF, LBO, Excel, Budgeting, Forecasting, Critical Thinking",
        "description": "Build institutional-grade DCF and leveraged buyout models to evaluate target technology acquisitions for private equity clients."
    },
    {
        "title": "Quantitative Risk & Derivatives Analyst",
        "company": "Sterling Risk Partners",
        "category": "FINANCE",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£80,000 - £105,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Quantitative Analysis, Python, Value at Risk (VaR), Stress Testing, Financial Derivatives, SQL, Statistics",
        "description": "Perform real-time portfolio stress testing across multi-currency fixed income and equity derivative holdings."
    },
    {
        "title": "Corporate FP&A Manager",
        "company": "Amazon Global Operations",
        "category": "FINANCE",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$135,000 - $170,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "FP&A, Budgeting, Variance Analysis, Forecasting, SQL, Financial Analysis, Executive Presentation",
        "description": "Direct financial planning cycles for regional fulfillment networks, forecasting quarterly OpEx and CapEx investments."
    },
    {
        "title": "Private Equity & M&A Associate",
        "company": "SoftBank Vision Fund",
        "category": "FINANCE",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£95,000 - £130,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Mergers & Acquisitions, Due Diligence, Financial Modeling, Cap Table Analysis, Negotiation, Strategic Planning",
        "description": "Evaluate late-stage tech startups, construct detailed revenue waterfalls, and prepare investment committee memorandums."
    },
    {
        "title": "Equity Research Analyst (Technology Sector)",
        "company": "ICICI Securities",
        "category": "FINANCE",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹16,00,000 - ₹26,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Equity Research, Financial Modeling, Valuation, Report Writing, Sector Analysis, Accounting",
        "description": "Publish institutional research notes on Indian IT services and SaaS companies, modeling quarterly earnings per share."
    },

    # ==================== 18. FITNESS ====================
    {
        "title": "Elite Athletic Performance & Strength Coach",
        "company": "Pulse Athletic Club",
        "category": "FITNESS",
        "loc": ("Melbourne", "Victoria", "Australia"),
        "salary_range": "A$78,000 - A$98,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Strength Training, Kinesiology, Nutrition, Exercise Physiology, Injury Prevention, CPR, Client Motivation",
        "description": "Design scientific periodization training blocks for competitive athletes and executives, monitoring biometric markers."
    },
    {
        "title": "Clinical Exercise Physiologist & Cardiac Rehab Coach",
        "company": "Mayo Clinic Health Network",
        "category": "FITNESS",
        "loc": ("Chicago", "Illinois", "United States"),
        "salary_range": "$75,000 - $95,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Exercise Physiology, Clinical Assessment, EKG Monitoring, Patient Care, Empathy, BLS",
        "description": "Prescribe and supervise outpatient physical rehabilitation regimens for cardiac recovery and orthopedic patients."
    },
    {
        "title": "Sports Nutrition & Dietetics Specialist",
        "company": "Equinox Luxury Wellness",
        "category": "FITNESS",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$80,000 - $105,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Nutrition, Meal Planning, Body Composition, Biochemical Tracking, Active Listening, Counseling",
        "description": "Formulate tailored macronutrient protocols and metabolic counseling sessions for high-performance club members."
    },
    {
        "title": "Functional Movement & Group Fitness Director",
        "company": "Cult.fit Healthcare",
        "category": "FITNESS",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹9,00,000 - ₹15,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Group Fitness, HIIT, Functional Training, Injury Prevention, Trainer Mentoring, Public Speaking",
        "description": "Lead high-energy fitness masterclasses, audit trainer movement standards, and develop proprietary workout formats."
    },
    {
        "title": "Corporate Wellness & Movement Lead",
        "company": "Nike World Headquarters",
        "category": "FITNESS",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$90,000 - $118,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Wellness Coaching, Ergonomics, Program Design, Stress Management, Community Engagement, Leadership",
        "description": "Develop and lead holistic wellness initiatives, desk ergonomics workshops, and annual fitness challenges for 8,000 staff."
    },

    # ==================== 19. HEALTHCARE ====================
    {
        "title": "Healthcare Clinical Data Scientist",
        "company": "BioGenix Health Systems",
        "category": "HEALTHCARE",
        "loc": ("Boston", "Massachusetts", "United States"),
        "salary_range": "$135,000 - $170,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Clinical Data, Python, EMR, EHR, Biostatistics, HIPAA Compliance, SQL, Predictive Modeling",
        "description": "Analyze clinical trial outcomes and ICU telemetry data, developing predictive algorithms for patient readmission risk."
    },
    {
        "title": "Hospital Operations & Quality Accreditation Lead",
        "company": "Apollo Hospitals Group",
        "category": "HEALTHCARE",
        "loc": ("Chennai", "Tamil Nadu", "India"),
        "salary_range": "₹12,00,000 - ₹18,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Healthcare Administration, NABH Standards, Patient Safety, Clinical Workflows, Quality Improvement, Leadership",
        "description": "Standardize patient safety protocols across a 500-bed tertiary facility, leading NABH and JCI accreditation audits."
    },
    {
        "title": "Critical Care Clinical Nurse Supervisor",
        "company": "NHS Foundation Trust",
        "category": "HEALTHCARE",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£48,000 - £65,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Nursing, Patient Care, Critical Care, Triage, BLS, ACLS, Empathy, Team Leadership, Crisis Management",
        "description": "Manage nursing shifts within a high-acuity intensive care unit, administering complex medication infusions."
    },
    {
        "title": "Clinical Research Coordinator (Oncology)",
        "company": "Pfizer Global R&D",
        "category": "HEALTHCARE",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$85,000 - $115,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Clinical Trials, GCP Guidelines, Patient Screening, IRB Documentation, Data Integrity, Communication",
        "description": "Coordinate Phase II and III oncology clinical drug trials, ensure patient informed consent, and record adverse events."
    },
    {
        "title": "Healthcare Informatics & Epic EHR Specialist",
        "company": "Kaiser Permanente",
        "category": "HEALTHCARE",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$115,000 - $145,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Epic Systems, EHR, Healthcare IT, Workflow Optimization, Clinical Documentation, Training",
        "description": "Customize Epic ambulatory modules, optimize physician order-entry templates, and train clinical staff."
    },

    # ==================== 20. HR (HUMAN RESOURCES) ====================
    {
        "title": "Lead Technical Talent Acquisition Partner",
        "company": "HyperScale AI Labs",
        "category": "HR",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$125,000 - $155,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Talent Acquisition, Technical Recruiting, Sourcing, Sourcing Algorithms, Interviewing, Offer Negotiation",
        "description": "Drive end-to-end recruitment for high-growth generative AI and infrastructure teams from outreach to offer closure."
    },
    {
        "title": "People Operations & HR Business Partner",
        "company": "Zenith Global Technologies",
        "category": "HR",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹14,00,000 - ₹20,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Employee Relations, HR Policies, Performance Management, HRMS, Talent Development, Retention Strategies",
        "description": "Partner with VP of Engineering to design career ladders, manage annual performance calibrations, and drive retention."
    },
    {
        "title": "Global Compensation & Total Rewards Analyst",
        "company": "Google Europe",
        "category": "HR",
        "loc": ("Zurich", "Zurich", "Switzerland"),
        "salary_range": "CHF 115,000 - CHF 145,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Compensation and Benefits, Market Benchmarking, Equity Grants, Data Analysis, Excel, Workforce Planning",
        "description": "Model cross-country salary bands and equity equity compensation structures across 14 European markets."
    },
    {
        "title": "Director of Organizational Learning & Leadership",
        "company": "Unilever Global",
        "category": "HR",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£85,000 - £115,000",
        "job_type": "Full-time",
        "experience_required": "Senior (6+ yrs)",
        "required_skills": "Leadership Development, Talent Development, Instructional Design, Executive Coaching, Strategic Planning",
        "description": "Design executive leadership accelerator academies, driving global talent development for senior leaders."
    },
    {
        "title": "Employee Relations & Labor Compliance Specialist",
        "company": "Tata Sons Enterprise",
        "category": "HR",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹12,00,000 - ₹17,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Labor Laws, Industrial Relations, Grievance Handling, Conflict Resolution, Policy Drafting, Mediation",
        "description": "Investigate workplace conduct complaints, ensure compliance with statutory labor laws, and lead formal mediation sessions."
    },

    # ==================== 21. INFORMATION-TECHNOLOGY ====================
    {
        "title": "Senior AI & Machine Learning Engineer",
        "company": "DeepPulse Labs",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$170,000 - $220,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Python, PyTorch, TensorFlow, LLMs, NLP, Docker, AWS, MLOps, SQL, Problem Solving",
        "description": "Architect and deploy generative AI pipelines, fine-tune transformer models, and optimize inference latency for enterprise."
    },
    {
        "title": "Full Stack Cloud Platform Developer",
        "company": "Nexus Technologies",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹20,00,000 - ₹30,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Python, React, TypeScript, FastAPI, PostgreSQL, Docker, AWS, Git, Teamwork",
        "description": "Build high-throughput web applications, microservices, and reactive user interfaces for global FinTech clients."
    },
    {
        "title": "DevOps & Cloud Infrastructure Architect",
        "company": "CloudForge Systems",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$145,000 - $185,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Kubernetes, Docker, Terraform, AWS, CI/CD, Linux, Python, Prometheus, Troubleshooting",
        "description": "Manage multi-cloud infrastructure, automate zero-downtime deployment pipelines, and strengthen cluster security."
    },
    {
        "title": "Lead Distributed Backend Systems Engineer",
        "company": "FinVector Trading",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£85,000 - £115,000",
        "job_type": "Hybrid",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Go, Python, Java, Kafka, Microservices, Redis, PostgreSQL, Distributed Systems",
        "description": "Design resilient trading ledger engines with sub-millisecond execution times and fault-tolerant architecture."
    },
    {
        "title": "Cybersecurity & SOC Incident Response Analyst",
        "company": "SecureNet Global",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Berlin", "Berlin", "Germany"),
        "salary_range": "€78,000 - €102,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Network Security, SIEM, Penetration Testing, Python, Incident Response, ISO 27001",
        "description": "Protect critical enterprise assets, conduct threat hunting, and implement SOC response workflows across EU operations."
    },
    {
        "title": "Lead Mobile Architect (Flutter & React Native)",
        "company": "AppFlow Studios",
        "category": "INFORMATION-TECHNOLOGY",
        "loc": ("Pune", "Maharashtra", "India"),
        "salary_range": "₹15,00,000 - ₹24,00,000",
        "job_type": "Full-time",
        "experience_required": "Junior-Mid (2-5 yrs)",
        "required_skills": "Flutter, React Native, Swift, Kotlin, REST APIs, Git, Firebase, UI/UX",
        "description": "Create cross-platform mobile apps with silky 60fps animations, offline sync capabilities, and push notifications."
    },

    # ==================== 22. PUBLIC-RELATIONS ====================
    {
        "title": "Corporate Communications & Media Director",
        "company": "Edelman Communications",
        "category": "PUBLIC-RELATIONS",
        "loc": ("New York", "New York", "United States"),
        "salary_range": "$130,000 - $170,000",
        "job_type": "Hybrid",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "Press Releases, Media Relations, Crisis Communication, Branding, Public Speaking, Storytelling",
        "description": "Formulate global PR strategies, build relationships with top-tier financial journalists, and lead press briefings."
    },
    {
        "title": "Crisis Communication & Reputation Strategist",
        "company": "Brunswick Group",
        "category": "PUBLIC-RELATIONS",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£75,000 - £100,000",
        "job_type": "Full-time",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Crisis Communication, Reputation Management, Stakeholder Communication, Media Training, Rapid Response",
        "description": "Advise FTSE 100 executive boards on urgent corporate crisis responses, cybersecurity incidents, and regulatory issues."
    },
    {
        "title": "Technology PR & Brand Evangelist",
        "company": "Weber Shandwick",
        "category": "PUBLIC-RELATIONS",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$100,000 - $135,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-5 yrs)",
        "required_skills": "Media Relations, Product Launches, Storytelling, Tech Journalism, Influencer Relations, Copywriting",
        "description": "Orchestrate product launch media tours for breakthrough AI companies, securing coverage in TechCrunch and Bloomberg."
    },
    {
        "title": "Public Affairs & Media Engagement Lead",
        "company": "Tata Group Corporate Affairs",
        "category": "PUBLIC-RELATIONS",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹15,00,000 - ₹22,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Public Affairs, Press Conferences, Government Relations, Speechwriting, Strategic Communications",
        "description": "Author executive speeches, draft op-eds, coordinate national media interviews, and support social outreach initiatives."
    },
    {
        "title": "Consumer Brand PR & Event Experience Manager",
        "company": "Ogilvy PR",
        "category": "PUBLIC-RELATIONS",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹11,00,000 - ₹17,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Event Planning, Brand Storytelling, Influencer Marketing, Press Releases, Relationship Building",
        "description": "Organize large-scale brand experiential pop-ups, manage celebrity brand ambassadors, and generate organic coverage."
    },

    # ==================== 23. SALES ====================
    {
        "title": "Enterprise SaaS Account Executive",
        "company": "Snowflake Data Cloud",
        "category": "SALES",
        "loc": ("Austin", "Texas", "United States"),
        "salary_range": "$140,000 - $190,000 + OTE",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "B2B Sales, Salesforce, Pipeline Management, Contract Negotiation, Cold Outreach, Closing Deals",
        "description": "Prospect and close six-figure annual recurring revenue deals with Fortune 1000 technical decision makers."
    },
    {
        "title": "Regional Commercial Sales Director",
        "company": "GlobalTrade Connect",
        "category": "SALES",
        "loc": ("Singapore", "Central", "Singapore"),
        "salary_range": "S$100,000 - S$140,000 + OTE",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-7 yrs)",
        "required_skills": "B2B Sales, Relationship Building, Sales Leadership, Negotiation, Presentation Skills, Client Acquisition",
        "description": "Expand commercial sales channels across Southeast Asia, exceed quarterly quotas, and manage senior client accounts."
    },
    {
        "title": "Inside Sales & Business Development Specialist",
        "company": "Razorpay Partner Group",
        "category": "SALES",
        "loc": ("Mumbai", "Maharashtra", "India"),
        "salary_range": "₹9,00,000 - ₹15,00,000 + Incentive",
        "job_type": "Full-time",
        "experience_required": "Junior (1-3 yrs)",
        "required_skills": "Lead Qualification, Cold Calling, CRM, Objection Handling, Product Demos, Active Listening",
        "description": "Engage SME founders and e-commerce merchants to demonstrate digital payment solutions, maintaining high conversion rates."
    },
    {
        "title": "Strategic Enterprise Account Director",
        "company": "Datadog Cloud Monitoring",
        "category": "SALES",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£90,000 - £130,000 + OTE",
        "job_type": "Hybrid",
        "experience_required": "Senior (5+ yrs)",
        "required_skills": "Enterprise Sales, Account Management, Cloud Technologies, Client Retention, Negotiation, Executive Presence",
        "description": "Lead multi-million pound renewal and cross-sell expansion across tier-1 European financial institutions."
    },
    {
        "title": "Inbound Sales & Solutions Consultant",
        "company": "HubSpot Inbound",
        "category": "SALES",
        "loc": ("Boston", "Massachusetts", "United States"),
        "salary_range": "$85,000 - $115,000 + OTE",
        "job_type": "Remote",
        "experience_required": "Junior-Mid (2-4 yrs)",
        "required_skills": "Inbound Sales, Consultative Selling, CRM, Solution Demonstration, Closing Deals, Active Listening",
        "description": "Guide inbound marketing prospects through technical product demonstrations, aligning software features to revenue goals."
    },

    # ==================== 24. TEACHER ====================
    {
        "title": "Computer Science & Artificial Intelligence Educator",
        "company": "NextGen STEM Academy",
        "category": "TEACHER",
        "loc": ("Seattle", "Washington", "United States"),
        "salary_range": "$85,000 - $110,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Python, Curriculum Development, Lesson Planning, Computer Science, Mentorship, Classroom Management",
        "description": "Deliver engaging masterclasses in Python programming and algorithmic thinking, mentoring high school student capstones."
    },
    {
        "title": "Senior Mathematics & Statistics Lecturer",
        "company": "Imperial College London",
        "category": "TEACHER",
        "loc": ("London", "Greater London", "United Kingdom"),
        "salary_range": "£50,000 - £70,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (3-6 yrs)",
        "required_skills": "Pedagogy, Statistics, Calculus, Student Assessment, Academic Advising, Public Speaking, Patience",
        "description": "Instruct undergraduate students in probability, linear algebra, and statistical inference, creating interactive modules."
    },
    {
        "title": "STEM Curriculum Specialist & Instructional Designer",
        "company": "Khan Academy EdTech",
        "category": "TEACHER",
        "loc": ("San Francisco", "California", "United States"),
        "salary_range": "$95,000 - $125,000",
        "job_type": "Remote",
        "experience_required": "Mid-Level (3-6 yrs)",
        "required_skills": "Instructional Design, Curriculum Development, E-Learning, Assessment Design, Pedagogy, Video Teaching",
        "description": "Architect accessible digital math and science micro-lessons reaching millions of students worldwide."
    },
    {
        "title": "Senior Physics Faculty & JEE Mentor",
        "company": "IIT Scholars Foundation",
        "category": "TEACHER",
        "loc": ("New Delhi", "Delhi", "India"),
        "salary_range": "₹15,00,000 - ₹24,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Senior (4-8 yrs)",
        "required_skills": "Physics, Competitive Exam Prep, Pedagogy, Problem Solving, Student Mentorship, Classroom Management",
        "description": "Teach advanced mechanics and electrodynamics to aspiring engineering scholars, mentoring students to national top ranks."
    },
    {
        "title": "Special Education & Behavioral Learning Specialist",
        "company": "Oakridge International School",
        "category": "TEACHER",
        "loc": ("Bengaluru", "Karnataka", "India"),
        "salary_range": "₹8,00,000 - ₹13,00,000",
        "job_type": "Full-time",
        "experience_required": "Mid-Level (2-5 yrs)",
        "required_skills": "Special Education, Individualized Education Programs (IEP), Empathy, Behavioral Therapy, Active Listening",
        "description": "Formulate tailored IEP learning plans for neurodiverse learners, coordinating with parents and classroom teachers."
    }
]

def seed_database():
    """Initializes tables and seeds worldwide job entries across ALL 24 categories."""
    try:
        from database.db import init_db
    except ModuleNotFoundError:
        from db import init_db
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    
    # Check distinct categories in the database
    cursor.execute("SELECT DISTINCT category FROM jobs")
    existing_cats = {r["category"] for r in cursor.fetchall()}
    
    # Check total count
    cursor.execute("SELECT COUNT(*) as cnt FROM jobs")
    total_count = cursor.fetchone()["cnt"]

    # If count is less than 100 or missing categories, populate all categories
    from config import KAGGLE_CATEGORIES
    missing_cats = [c for c in KAGGLE_CATEGORIES if c not in existing_cats]

    if total_count < 100 or missing_cats:
        print(f"Populating full jobs database across all 24 categories (currently {total_count} jobs, missing {len(missing_cats)} categories)...")
        # Clear old subset to insert comprehensive set
        cursor.execute("DELETE FROM jobs")
        conn.commit()

        inserted_count = 0
        for job in ALL_FIELD_JOBS:
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
            inserted_count += 1
        print(f"Successfully seeded {inserted_count} jobs across ALL 24 Kaggle categories.")
    else:
        print(f"Database already contains {total_count} jobs across all fields.")
    conn.close()

if __name__ == "__main__":
    seed_database()
