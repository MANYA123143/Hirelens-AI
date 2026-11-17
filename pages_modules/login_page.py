"""
HireLens AI - Authentication & Registration UI
Ultra-fast, mobile-responsive, modern sign-in & registration experience.
"""
import streamlit as st
from database.db import authenticate_user, register_user
from config import KAGGLE_CATEGORIES
from core.notification_engine import sync_user_job_notifications

def render_login_page():
    st.markdown("""
    <div style="text-align: center; padding: 20px 10px 10px 10px; margin-bottom: 20px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 16px; font-size: 28px; margin-bottom: 12px; box-shadow: 0 0 25px rgba(59, 130, 246, 0.35);">
            🎯
        </div>
        <h1 style="font-size: 34px; font-weight: 800; color: #60A5FA; margin: 0; letter-spacing: -0.5px;">
            HireLens AI
        </h1>
        <p style="font-size: 14.5px; color: #94A3B8; max-width: 600px; margin: 8px auto 0 auto; line-height: 1.5;">
            AI Resume Analysis, ATS Audit, Custom Resume Maker & Global Job Opportunities with Proximity Alerts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔐 Sign In to Account", "✨ Create Free Account (Candidate)"])

    # ==================== SIGN IN TAB ====================
    with tab_login:
        st.subheader("Welcome Back")
        st.write("Sign in to access your ATS scoring audit, saved resumes, and local job matching radar.")

        login_id = st.text_input("Username or Email", key="login_id", placeholder="e.g. alex.chen@example.com")
        password = st.text_input("Password", type="password", key="login_pwd", placeholder="••••••••")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🚀 Log In to HireLens", use_container_width=True, type="primary"):
                if not login_id or not password:
                    st.error("Please enter both username/email and password.")
                else:
                    user = authenticate_user(login_id, password)
                    if user:
                        st.session_state["user"] = user
                        st.session_state["logged_in"] = True
                        sync_user_job_notifications(user)
                        st.success(f"Welcome back, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

        with col2:
            st.write("**Instant 1-Click Demo Logins:**")
            demo_col_a, demo_col_b = st.columns(2)
            with demo_col_a:
                if st.button("👨‍🎓 Student Demo (US)", use_container_width=True):
                    demo_user = authenticate_user("demo_student", "Demo@123")
                    if not demo_user:
                        register_user(
                            username="demo_student",
                            email="student@hirelens.ai",
                            password="Demo@123",
                            full_name="Alex Mercer (Student)",
                            phone="+1 (415) 890-1234",
                            city="San Francisco",
                            state="California",
                            country="United States",
                            target_role="Full Stack AI Engineer",
                            target_category="INFORMATION-TECHNOLOGY",
                            skills="Python, SQL, React, Docker, FastAPI, Git, PyTorch",
                            experience_level="Student/Fresher",
                            lat=37.7749,
                            lon=-122.4194
                        )
                        demo_user = authenticate_user("demo_student", "Demo@123")
                    st.session_state["user"] = demo_user
                    st.session_state["logged_in"] = True
                    sync_user_job_notifications(demo_user)
                    st.rerun()

            with demo_col_b:
                if st.button("🇮🇳 India Candidate", use_container_width=True):
                    demo_in = authenticate_user("demo_bengaluru", "Demo@123")
                    if not demo_in:
                        register_user(
                            username="demo_bengaluru",
                            email="rahul.sharma@hirelens.ai",
                            password="Demo@123",
                            full_name="Rahul Sharma",
                            phone="+91 98765 43210",
                            city="Bengaluru",
                            state="Karnataka",
                            country="India",
                            target_role="Software Development Engineer",
                            target_category="INFORMATION-TECHNOLOGY",
                            skills="Python, Java, Spring Boot, React, SQL, AWS, Kubernetes",
                            experience_level="Junior (1-3 yrs)",
                            lat=12.9716,
                            lon=77.5946
                        )
                        demo_in = authenticate_user("demo_bengaluru", "Demo@123")
                    st.session_state["user"] = demo_in
                    st.session_state["logged_in"] = True
                    sync_user_job_notifications(demo_in)
                    st.rerun()

    # ==================== SIGN UP TAB ====================
    with tab_signup:
        st.subheader("New Registration")
        st.info("💡 Register your personal details so HireLens can automatically notify you whenever new job requirements matching your skills and location are posted!")

        with st.form("signup_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                full_name = st.text_input("Full Name *", placeholder="e.g. Maya Patel")
                username = st.text_input("Username *", placeholder="e.g. maya_p")
                email = st.text_input("Email Address *", placeholder="e.g. maya@example.com")
                phone = st.text_input("Phone Number *", placeholder="e.g. +1 555-019-2834 or +91 9876543210")
                password = st.text_input("Create Password *", type="password", placeholder="At least 6 characters")

            with col_b:
                city = st.text_input("City *", placeholder="e.g. Bengaluru / San Francisco / London")
                state = st.text_input("State / Province *", placeholder="e.g. Karnataka / California / Greater London")
                country = st.text_input("Country *", placeholder="e.g. India / United States / United Kingdom")
                target_role = st.text_input("Target Job Title *", placeholder="e.g. Machine Learning Engineer / Financial Analyst")
                experience_level = st.selectbox(
                    "Current Experience Level",
                    ["Student/Fresher (0 yrs)", "Junior (1-2 yrs)", "Mid-Level (3-5 yrs)", "Senior (5+ yrs)"]
                )

            st.markdown("---")
            st.markdown("#### 🎯 Domain & Skills Targeting")
            col_c, col_d = st.columns([1, 1])
            with col_c:
                target_category = st.selectbox(
                    "Primary Industry Category (from Kaggle Dataset)",
                    KAGGLE_CATEGORIES,
                    index=KAGGLE_CATEGORIES.index("INFORMATION-TECHNOLOGY") if "INFORMATION-TECHNOLOGY" in KAGGLE_CATEGORIES else 0
                )
            with col_d:
                skills = st.text_area(
                    "Your Key Skills (comma-separated) *",
                    placeholder="e.g. Python, SQL, React, AWS, Docker, Machine Learning, Git",
                    help="These skills will be matched in real-time against new job requirements to trigger notification pop-ups."
                )

            notif_toggle = st.checkbox(
                "🔔 Enable instant notification alerts when new jobs matching my skills & city/state are posted",
                value=True
            )

            submit_btn = st.form_submit_button("✨ Complete Registration & Enter Platform", type="primary", use_container_width=True)

            if submit_btn:
                if not (full_name and username and email and password and city and skills):
                    st.error("Please fill in all required fields marked with *.")
                elif len(password) < 5:
                    st.error("Password must be at least 5 characters.")
                else:
                    res = register_user(
                        username=username.strip().lower(),
                        email=email.strip().lower(),
                        password=password,
                        full_name=full_name.strip(),
                        phone=phone.strip(),
                        city=city.strip(),
                        state=state.strip(),
                        country=country.strip(),
                        target_role=target_role.strip(),
                        target_category=target_category,
                        skills=skills.strip(),
                        experience_level=experience_level
                    )
                    if res["success"]:
                        st.success("Account created successfully! Logging you in...")
                        user = authenticate_user(username, password)
                        st.session_state["user"] = user
                        st.session_state["logged_in"] = True
                        sync_user_job_notifications(user)
                        st.rerun()
                    else:
                        st.error(res["message"])
