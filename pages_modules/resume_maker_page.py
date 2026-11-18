"""
HireLens AI - AI Resume Maker (Blank Canvas for Students)
High-speed, mobile-responsive, blank canvas builder with AI bullet & summary polishers.
"""
import streamlit as st
try:
    from core.resume_generator import generate_ai_summary, enhance_bullet_point, build_resume_text, build_resume_html
    from database.db import save_user_resume
except ModuleNotFoundError:
    from resume_generator import generate_ai_summary, enhance_bullet_point, build_resume_text, build_resume_html
    from db import save_user_resume

def render_resume_maker():
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">
            📝 AI Resume Maker (Blank Canvas)
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 13.5px;">
            Fill in your details section by section. Use our instant AI helpers to polish action bullets and summaries, then export or test in the ATS analyzer.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})

    if "student_resume_data" not in st.session_state:
        st.session_state["student_resume_data"] = {
            "personal": {
                "full_name": user.get("full_name", ""),
                "title": user.get("target_role", ""),
                "email": user.get("email", ""),
                "phone": user.get("phone", ""),
                "city": user.get("city", ""),
                "state": user.get("state", ""),
                "country": user.get("country", ""),
                "linkedin": "https://linkedin.com/in/",
                "github": "https://github.com/",
                "portfolio": ""
            },
            "summary": "",
            "skills": {
                "Languages": "Python, SQL, JavaScript",
                "Frameworks": "React, FastAPI, Docker",
                "Tools & Cloud": "Git, AWS, Linux, GitHub Actions",
                "Soft Skills": "Problem Solving, Agile, Technical Writing"
            },
            "experience": [
                {
                    "role": "Software Engineering Intern",
                    "company": "Tech Innovations Inc.",
                    "location": f"{user.get('city', 'San Francisco')}, {user.get('state', 'CA')}",
                    "dates": "May 2024 - Aug 2024",
                    "bullets": "Engineered automated data ingestion pipeline using Python and SQL.\nCollaborated with senior engineers in bi-weekly Agile sprints to deliver REST APIs."
                }
            ],
            "education": [
                {
                    "degree": "B.S. in Computer Science",
                    "institution": "University School of Engineering",
                    "year": "2021 - 2025",
                    "gpa": "3.8 / 4.0",
                    "coursework": "Data Structures, Algorithms, Cloud Computing, Database Systems"
                }
            ],
            "projects": [
                {
                    "title": "HireLens AI Platform",
                    "tech_stack": "Python, Streamlit, SQLite, Scikit-learn",
                    "link": "https://github.com/project-demo",
                    "description": "Architected an end-to-end AI resume analysis and job matching application.\nImplemented multi-factor ATS scoring algorithm analyzing keyword taxonomy and readability."
                }
            ],
            "certifications": "AWS Certified Cloud Practitioner (2024)\nGitHub Foundations Certification"
        }

    resume_data = st.session_state["student_resume_data"]

    # Action Toolbar
    tb1, tb2, tb3 = st.columns([1, 1, 1])
    with tb1:
        if st.button("🧹 Clear All (100% Blank)", use_container_width=True):
            st.session_state["student_resume_data"] = {
                "personal": {"full_name": "", "title": "", "email": "", "phone": "", "city": "", "state": "", "country": "", "linkedin": "", "github": "", "portfolio": ""},
                "summary": "",
                "skills": {"Languages": "", "Frameworks": "", "Tools & Cloud": "", "Soft Skills": ""},
                "experience": [{"role": "", "company": "", "location": "", "dates": "", "bullets": ""}],
                "education": [{"degree": "", "institution": "", "year": "", "gpa": "", "coursework": ""}],
                "projects": [{"title": "", "tech_stack": "", "link": "", "description": ""}],
                "certifications": ""
            }
            st.rerun()

    with tb2:
        if st.button("📋 Load Sample Student Profile", use_container_width=True):
            st.session_state["student_resume_data"] = {
                "personal": {
                    "full_name": "Alex Mercer",
                    "title": "Junior Full Stack & AI Developer",
                    "email": "alex.mercer@example.com",
                    "phone": "+1 (415) 890-1234",
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States",
                    "linkedin": "https://linkedin.com/in/alex-mercer",
                    "github": "https://github.com/alex-mercer",
                    "portfolio": "https://alexmercer.dev"
                },
                "summary": "Ambitious Computer Science graduate with hands-on expertise in Python, React, SQL, and Docker. Proven ability to build production-grade web APIs and machine learning pipelines. Eager to contribute to scalable cloud architectures.",
                "skills": {
                    "Languages": "Python, TypeScript, SQL, JavaScript, HTML/CSS",
                    "Frameworks": "React, FastAPI, Node.js, Scikit-learn, Tailwind CSS",
                    "Tools & Cloud": "Docker, AWS, Git, Linux, PostgreSQL, Redis",
                    "Soft Skills": "Agile Development, Problem Solving, Cross-Functional Collaboration"
                },
                "experience": [
                    {
                        "role": "Software Developer Intern",
                        "company": "Apex Cloud Systems",
                        "location": "San Francisco, CA",
                        "dates": "June 2024 - Sept 2024",
                        "bullets": "Spearheaded refactoring of backend microservices using FastAPI, cutting API latency by 35%.\nEngineered automated CI/CD pipeline using GitHub Actions, decreasing deployment cycle time by 40%.\nCollaborated with product team to design accessible React frontend dashboards."
                    }
                ],
                "education": [
                    {
                        "degree": "B.S. in Computer Science",
                        "institution": "University of California, Berkeley",
                        "year": "2021 - 2025",
                        "gpa": "3.85 / 4.0",
                        "coursework": "Operating Systems, Distributed Systems, Machine Learning, Database Management"
                    }
                ],
                "projects": [
                    {
                        "title": "Smart ATS & Job Matchmaker",
                        "tech_stack": "Python, Streamlit, PyPDF, SQLite, Scikit-learn",
                        "link": "https://github.com/alex-mercer/smart-ats",
                        "description": "Built real-time resume parser evaluating keyword density and section completeness across 2,400+ benchmark profiles.\nIntegrated interactive world mapping displaying job opportunities with geo-spatial filtering."
                    }
                ],
                "certifications": "AWS Certified Solutions Architect – Associate (2024)\nDeepLearning.AI Machine Learning Specialization"
            }
            st.rerun()

    with tb3:
        if st.button("💾 Save to Profile History", use_container_width=True, type="secondary"):
            if user:
                save_user_resume(
                    user_id=user["id"],
                    resume_name=f"Created Resume - {resume_data['personal'].get('title', 'General')}",
                    resume_data_dict=resume_data,
                    ats_score=85.0,
                    category=user.get("target_category", "INFORMATION-TECHNOLOGY")
                )
                st.success("Resume saved to your profile!")
            else:
                st.warning("Sign in to save resumes to your persistent profile.")

    # Two column layout: Left is Form, Right is Live Preview
    tab_edit, tab_preview = st.tabs(["✍️ Edit Resume Sections", "👁️ Live ATS Resume Preview & Export"])

    with tab_edit:
        # 1. Personal Details
        with st.expander("👤 1. Personal & Contact Information", expanded=True):
            p = resume_data["personal"]
            c1, c2 = st.columns(2)
            with c1:
                p["full_name"] = st.text_input("Full Name *", value=p.get("full_name", ""))
                p["title"] = st.text_input("Professional Job Title *", value=p.get("title", ""), placeholder="e.g. Full Stack Developer")
                p["email"] = st.text_input("Email Address *", value=p.get("email", ""))
                p["phone"] = st.text_input("Phone Number *", value=p.get("phone", ""))
            with c2:
                p["city"] = st.text_input("City *", value=p.get("city", ""))
                p["state"] = st.text_input("State / Province *", value=p.get("state", ""))
                p["country"] = st.text_input("Country *", value=p.get("country", ""))
                p["linkedin"] = st.text_input("LinkedIn Profile URL", value=p.get("linkedin", ""))
                p["github"] = st.text_input("GitHub URL", value=p.get("github", ""))
                p["portfolio"] = st.text_input("Portfolio Website URL", value=p.get("portfolio", ""))

        # 2. Professional Summary
        with st.expander("📄 2. Professional Summary / Objective", expanded=True):
            col_s1, col_s2 = st.columns([3, 1])
            with col_s2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ AI Polish Summary", use_container_width=True):
                    all_skills = ", ".join([v for v in resume_data["skills"].values() if v])
                    resume_data["summary"] = generate_ai_summary(
                        target_role=resume_data["personal"].get("title", "Software Developer"),
                        top_skills=all_skills,
                        experience_level="Student/Fresher"
                    )
                    st.rerun()

            with col_s1:
                resume_data["summary"] = st.text_area(
                    "Professional Summary (3-4 impactful sentences)",
                    value=resume_data.get("summary", ""),
                    height=100,
                    placeholder="Write a concise overview highlighting your core competencies..."
                )

        # 3. Skills (Technical + Non-Technical / Soft Skills)
        with st.expander("🛠️ 3. Skills & Competencies (Technical & Non-Technical)", expanded=True):
            st.caption("Recruiters and ATS systems screen for both hard technical capabilities and essential non-technical/soft skills.")
            sk = resume_data["skills"]
            c_sk1, c_sk2 = st.columns(2)
            with c_sk1:
                st.markdown("**💻 Technical Skills**")
                sk["Languages"] = st.text_input("Programming / Core Tools", value=sk.get("Languages", ""), placeholder="e.g. Python, Java, SQL, Figma, AutoCAD, QuickBooks")
                sk["Frameworks"] = st.text_input("Frameworks, Cloud & DevOps", value=sk.get("Frameworks", ""), placeholder="e.g. React, Docker, AWS, FastAPI, Linux, Git")
            with c_sk2:
                st.markdown("**🤝 Non-Technical & Leadership Skills**")
                sk["Soft Skills"] = st.text_input("Soft & Interpersonal Skills", value=sk.get("Soft Skills", ""), placeholder="e.g. Communication, Active Listening, Teamwork, Empathy, Adaptability")
                sk["Tools & Cloud"] = st.text_input("Leadership, Management & Problem Solving", value=sk.get("Tools & Cloud", ""), placeholder="e.g. Leadership, Project Management, Agile, Critical Thinking, Negotiation")

        # 4. Experience
        with st.expander("💼 4. Work & Internship Experience", expanded=True):
            for i, exp in enumerate(resume_data["experience"]):
                st.markdown(f"**Experience #{i+1}**")
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    exp["role"] = st.text_input(f"Job / Internship Title #{i+1}", value=exp.get("role", ""))
                    exp["company"] = st.text_input(f"Company / Organization #{i+1}", value=exp.get("company", ""))
                with col_e2:
                    exp["location"] = st.text_input(f"Location #{i+1}", value=exp.get("location", ""))
                    exp["dates"] = st.text_input(f"Dates #{i+1}", value=exp.get("dates", ""))

                col_b1, col_b2 = st.columns([3, 1])
                with col_b2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"✨ AI Enhance Bullets #{i+1}", key=f"btn_enh_{i}"):
                        bullets = exp.get("bullets", "").split("\n")
                        enhanced = [enhance_bullet_point(b) for b in bullets if b.strip()]
                        exp["bullets"] = "\n".join(enhanced)
                        st.rerun()

                with col_b1:
                    exp["bullets"] = st.text_area(
                        f"Bullet Points (one per line) #{i+1}",
                        value=exp.get("bullets", ""),
                        height=100,
                        placeholder="• Spearheaded development of feature X, boosting throughput by 20%...\n• Collaborated with team to ship release on schedule..."
                    )
                st.markdown("---")

            if st.button("➕ Add Another Work Experience Entry"):
                resume_data["experience"].append({"role": "", "company": "", "location": "", "dates": "", "bullets": ""})
                st.rerun()

        # 5. Education
        with st.expander("🎓 5. Education History", expanded=True):
            for i, edu in enumerate(resume_data["education"]):
                st.markdown(f"**Education #{i+1}**")
                col_ed1, col_ed2 = st.columns(2)
                with col_ed1:
                    edu["degree"] = st.text_input(f"Degree & Major #{i+1}", value=edu.get("degree", ""), placeholder="e.g. B.S. in Computer Science")
                    edu["institution"] = st.text_input(f"College / University #{i+1}", value=edu.get("institution", ""))
                with col_ed2:
                    edu["year"] = st.text_input(f"Graduation Year #{i+1}", value=edu.get("year", ""), placeholder="e.g. 2021 - 2025")
                    edu["gpa"] = st.text_input(f"GPA / Percentage #{i+1}", value=edu.get("gpa", ""), placeholder="e.g. 3.8 / 4.0")
                edu["coursework"] = st.text_input(f"Relevant Coursework #{i+1}", value=edu.get("coursework", ""), placeholder="Data Structures, Algorithms, Machine Learning")
                st.markdown("---")

            if st.button("➕ Add Another Education Entry"):
                resume_data["education"].append({"degree": "", "institution": "", "year": "", "gpa": "", "coursework": ""})
                st.rerun()

        # 6. Projects
        with st.expander("🛠️ 6. Key Projects", expanded=True):
            for i, proj in enumerate(resume_data["projects"]):
                st.markdown(f"**Project #{i+1}**")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    proj["title"] = st.text_input(f"Project Title #{i+1}", value=proj.get("title", ""))
                    proj["tech_stack"] = st.text_input(f"Technologies Used #{i+1}", value=proj.get("tech_stack", ""), placeholder="e.g. Python, React, PostgreSQL")
                with col_p2:
                    proj["link"] = st.text_input(f"Demo / GitHub Link #{i+1}", value=proj.get("link", ""), placeholder="https://github.com/username/project")
                proj["description"] = st.text_area(f"Project Description & Highlights #{i+1}", value=proj.get("description", ""), height=80)
                st.markdown("---")

            if st.button("➕ Add Another Project"):
                resume_data["projects"].append({"title": "", "tech_stack": "", "link": "", "description": ""})
                st.rerun()

        # 7. Certifications
        with st.expander("📜 7. Certifications & Achievements", expanded=True):
            resume_data["certifications"] = st.text_area(
                "Certifications (one per line)",
                value=resume_data.get("certifications", ""),
                height=80,
                placeholder="AWS Certified Cloud Practitioner\nGoogle Data Analytics Professional Certificate"
            )

    # ==================== LIVE PREVIEW & EXPORT TAB ====================
    with tab_preview:
        resume_text_compiled = build_resume_text(resume_data)
        resume_html_compiled = build_resume_html(resume_data)

        # Action Buttons Header
        exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 1])
        with exp_col1:
            st.download_button(
                label="📥 Download Printable HTML / PDF",
                data=resume_html_compiled,
                file_name="HireLens_ATS_Resume.html",
                mime="text/html",
                use_container_width=True,
                type="primary"
            )
        with exp_col2:
            st.download_button(
                label="📄 Download Plain Text",
                data=resume_text_compiled,
                file_name="HireLens_ATS_Resume.txt",
                mime="text/plain",
                use_container_width=True
            )
        with exp_col3:
            if st.button("🚀 Test in AI ATS Checker", use_container_width=True):
                st.session_state["resume_to_analyze"] = resume_text_compiled
                st.session_state["current_page"] = "ats_analyzer"
                st.rerun()

        st.caption("💡 Tip: To save as a clean PDF, click 'Download Printable HTML / PDF', open it in your browser, and press `Ctrl+P` (Print to PDF).")

        # Live HTML Preview Container
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.components.v1.html(resume_html_compiled, height=850, scrolling=True)
