"""
HireLens AI - Candidate Profile & Personal Details Management
Manages user contact info, skills, location preferences, notification settings, and saved resumes.
"""
import streamlit as st
try:
    from database.db import update_user_profile, get_user_by_id, get_user_notifications, mark_all_notifications_read, get_user_resumes, create_notification
    from database.seed_data import WORLD_CITIES
except ModuleNotFoundError:
    from db import update_user_profile, get_user_by_id, get_user_notifications, mark_all_notifications_read, get_user_resumes, create_notification
    from seed_data import WORLD_CITIES
from config import KAGGLE_CATEGORIES

def render_profile_page():
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #1e3a8a; margin-bottom: 4px;">
            👤 Candidate Profile & Notification Preferences
        </h2>
        <p style="color: #64748b; margin: 0;">
            Keep your personal details, location, and skills updated so that HireLens can trigger accurate job alerts for you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")
    if not user:
        st.warning("Please sign in.")
        return

    # Refresh user from database
    user = get_user_by_id(user["id"])
    st.session_state["user"] = user

    tab_profile, tab_notifs, tab_saved = st.tabs([
        "⚙️ Edit Personal Details & Skills",
        "🔔 Notification Alert Center",
        "📂 Saved Resumes & ATS History"
    ])

    # ==================== EDIT PROFILE TAB ====================
    with tab_profile:
        with st.form("profile_form"):
            st.subheader("Personal & Contact Details")
            c1, c2 = st.columns(2)
            with c1:
                full_name = st.text_input("Full Name", value=user.get("full_name", ""))
                email = st.text_input("Email Address", value=user.get("email", ""), disabled=True, help="Email is your unique identifier.")
                phone = st.text_input("Phone Number", value=user.get("phone", ""))
                target_role = st.text_input("Target Job Title", value=user.get("target_role", ""))

            with c2:
                city = st.text_input("City", value=user.get("city", ""))
                state = st.text_input("State / Province", value=user.get("state", ""))
                country = st.text_input("Country", value=user.get("country", ""))
                
                cat_idx = 0
                if user.get("target_category") in KAGGLE_CATEGORIES:
                    cat_idx = KAGGLE_CATEGORIES.index(user.get("target_category"))
                target_category = st.selectbox("Target Category (from Kaggle Dataset)", KAGGLE_CATEGORIES, index=cat_idx)

            st.markdown("---")
            st.subheader("Skills & Alert Triggers")
            skills = st.text_area(
                "Your Skills (comma-separated)",
                value=user.get("skills", ""),
                help="HireLens matches these skills in real-time against new job postings in your city and state."
            )

            exp_options = ["Student/Fresher (0 yrs)", "Junior (1-2 yrs)", "Mid-Level (3-5 yrs)", "Senior (5+ yrs)"]
            curr_exp = user.get("experience_level", "Student/Fresher (0 yrs)")
            exp_idx = exp_options.index(curr_exp) if curr_exp in exp_options else 0
            experience_level = st.selectbox("Experience Level", exp_options, index=exp_idx)

            notif_enabled = st.checkbox(
                "🔔 Enable instant notification pop-up alerts when new jobs matching my skills & city are posted",
                value=bool(user.get("notifications_enabled", 1))
            )

            save_btn = st.form_submit_button("💾 Save Profile Changes", type="primary", use_container_width=True)

            if save_btn:
                # Update coordinates if city/state provided
                coords = WORLD_CITIES.get((city.strip(), state.strip(), country.strip()), (0.0, 0.0))
                update_user_profile(
                    user["id"],
                    full_name=full_name.strip(),
                    phone=phone.strip(),
                    city=city.strip(),
                    state=state.strip(),
                    country=country.strip(),
                    latitude=coords[0],
                    longitude=coords[1],
                    target_role=target_role.strip(),
                    target_category=target_category,
                    skills=skills.strip(),
                    experience_level=experience_level,
                    notifications_enabled=1 if notif_enabled else 0
                )
                # Refresh session state
                st.session_state["user"] = get_user_by_id(user["id"])
                st.success("✅ Profile updated successfully! Job match alerts will now reflect your updated preferences.")
                st.rerun()

    # ==================== NOTIFICATIONS TAB ====================
    with tab_notifs:
        st.subheader("🔔 Notification History")
        notifications = get_user_notifications(user["id"], limit=30)
        
        col_nt1, col_nt2 = st.columns([1, 1])
        with col_nt1:
            if st.button("Mark All Notifications as Read", use_container_width=True):
                mark_all_notifications_read(user["id"])
                st.rerun()

        with col_nt2:
            if st.button("⚡ Test Instant Notification Pop-up Alert", use_container_width=True, type="secondary"):
                test_title = f"🔔 Test Alert: Urgent Opening in {user.get('city', 'Your City')}!"
                test_msg = f"A new high-priority position matching your skills ({user.get('skills', 'Tech')}) was just logged in {user.get('city', 'Local Area')}."
                create_notification(
                    user_id=user["id"],
                    job_id=None,
                    title=test_title,
                    message=test_msg,
                    matched_skills=user.get("skills", "")
                )
                st.toast("🔔 Test Notification Pop-up Triggered!", icon="✨")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if not notifications:
            st.info("No notifications logged yet. When new jobs match your skills, alerts will appear here and on your dashboard.")
        else:
            for n in notifications:
                status_icon = "⚪ Read" if n["is_read"] else "🟢 **New Unread**"
                card_bg = "#f8fafc" if n["is_read"] else "#eff6ff"
                border_color = "#cbd5e1" if n["is_read"] else "#2563eb"
                
                st.markdown(f"""
                <div style="background: {card_bg}; border: 1px solid {border_color}; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #0f172a; font-size: 15px;">{n['title']}</span>
                        <span style="font-size: 12px; color: #64748b;">{n['created_at']} &nbsp;|&nbsp; {status_icon}</span>
                    </div>
                    <div style="font-size: 13px; color: #334155; margin-top: 6px;">
                        {n['message']}
                    </div>
                    {f"<div style='font-size: 12px; color: #0d9488; margin-top: 4px;'><strong>Matched Skills:</strong> {n['matched_skills']}</div>" if n.get('matched_skills') else ""}
                </div>
                """, unsafe_allow_html=True)

    # ==================== SAVED RESUMES TAB ====================
    with tab_saved:
        st.subheader("📂 Saved Resumes & ATS History")
        resumes = get_user_resumes(user["id"])
        
        if not resumes:
            st.info("No resumes saved yet. Build one in the **AI Resume Maker** or test in the **ATS Analyzer** to save.")
        else:
            for r in resumes:
                score_str = f"Score: {r['ats_score']}%" if r['ats_score'] else "Not Scored"
                score_color = "#10b981" if (r['ats_score'] or 0) >= 80 else "#2563eb"
                
                with st.expander(f"📄 {r['resume_name']} ({r['created_at']}) - {score_str}"):
                    st.markdown(f"**Target Category:** {r.get('target_category', 'General')}")
                    st.markdown(f"**ATS Score:** <span style='color: {score_color}; font-weight: 700;'>{score_str}</span>", unsafe_allow_html=True)
                    if st.button("Load this Resume into ATS Checker", key=f"load_res_{r['id']}"):
                        # Extract text
                        res_data = r.get("data", {})
                        from core.resume_generator import build_resume_text
                        if isinstance(res_data, dict) and "personal" in res_data:
                            txt = build_resume_text(res_data)
                        elif "text" in res_data:
                            txt = res_data["text"]
                        else:
                            txt = str(res_data)
                        st.session_state["resume_to_analyze"] = txt
                        st.session_state["current_page"] = "ats_analyzer"
                        st.rerun()
