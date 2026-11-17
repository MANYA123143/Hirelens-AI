"""
HireLens AI - Candidate Dashboard & Real-Time Alert Hub
High-speed, mobile-responsive, vibrant career command center.
"""
import streamlit as st
try:
    from database.db import get_user_notifications, mark_notification_read, get_jobs_near_user
    from core.notification_engine import match_jobs_for_candidate, sync_user_job_notifications
except ModuleNotFoundError:
    from db import get_user_notifications, mark_notification_read, get_jobs_near_user
    from notification_engine import match_jobs_for_candidate, sync_user_job_notifications

def render_dashboard():
    user = st.session_state.get("user", {})
    if not user:
        st.warning("Please sign in first.")
        return

    # Check for notification alerts
    notifications = get_user_notifications(user["id"], limit=5)
    unread_notifs = [n for n in notifications if not n["is_read"]]

    # ==================== REAL-TIME NOTIFICATION POP-UP BANNER ====================
    if unread_notifs:
        latest = unread_notifs[0]
        st.markdown(f"""
        <div class="notification-banner">
            <div class="notification-title">
                <span>🔥 LIVE JOB MATCH ALERT ({len(unread_notifs)} New)</span>
                <span class="live-indicator" style="margin-left: auto;">
                    <span class="live-dot"></span> MATCHING NOW
                </span>
            </div>
            <div class="notification-body">
                <strong>{latest['title']}</strong><br>
                {latest['message']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("Mark Alert as Read", key="dismiss_notif_btn", use_container_width=True):
                mark_notification_read(latest["id"])
                st.rerun()
        with col_n2:
            if st.button("🗺️ View Match on World Map", key="jump_job_btn", type="primary", use_container_width=True):
                st.session_state["current_page"] = "job_opportunities"
                st.rerun()

    # ==================== HERO COMMAND BANNER ====================
    city = user.get("city", "Your City")
    state = user.get("state", "Your State")
    country = user.get("country", "")
    loc_str = f"{city}, {state}" if state else city
    if country: loc_str += f" ({country})"

    st.markdown(f"""
    <div class="hirelens-hero">
        <div class="hero-title">
            <span>Welcome, {user.get('full_name', 'Professional')}! 👋</span>
            <span class="live-indicator"><span class="live-dot"></span> RADAR ACTIVE</span>
        </div>
        <div class="hero-subtitle">
            🎯 Target Role: <strong style="color: #60A5FA;">{user.get('target_role', 'Specialist')}</strong> &nbsp;•&nbsp; 
            📍 Location: <strong style="color: #34D399;">{loc_str}</strong> &nbsp;•&nbsp; 
            🏷️ Industry: <strong style="color: #C084FC;">{user.get('target_category', 'Tech')}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==================== VIBRANT STATS ROW ====================
    local_jobs = get_jobs_near_user(user.get("city", ""), user.get("state", ""), user.get("country", ""))
    skill_matches = match_jobs_for_candidate(user, min_match_pct=30.0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #3B82F6;">{len(local_jobs)}</div>
            <div class="stat-lbl">Jobs in {user.get('city', 'Your City')} / State</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #10B981;">{len(skill_matches)}</div>
            <div class="stat-lbl">Skill-Matched Positions</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        skills_count = len([s for s in user.get('skills', '').split(',') if s.strip()])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #8B5CF6;">{skills_count}</div>
            <div class="stat-lbl">Candidate Skills Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #F43F5E;">{len(unread_notifs)}</div>
            <div class="stat-lbl">Pending Alert Triggers</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== QUICK ACTION HUBS ====================
    st.subheader("⚡ Quick Launchpad")
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        with st.container(border=True):
            st.markdown("#### 🎯 AI ATS Analyzer")
            st.caption("Scan your resume against 24 Kaggle dataset categories and calculate your ATS score.")
            if st.button("Launch ATS Checker", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "ats_analyzer"
                st.rerun()

    with q2:
        with st.container(border=True):
            st.markdown("#### 📝 Blank Resume Maker")
            st.caption("Fill in a clean blank canvas with AI bullet enhancers & summary generators.")
            if st.button("Open Resume Maker", use_container_width=True):
                st.session_state["current_page"] = "resume_maker"
                st.rerun()

    with q3:
        with st.container(border=True):
            st.markdown("#### 🗺️ World Job Map")
            st.caption("Discover nearby jobs in your city/state or navigate 3D hiring hubs across the world.")
            if st.button("Explore World Map", use_container_width=True):
                st.session_state["current_page"] = "job_opportunities"
                st.rerun()

    with q4:
        with st.container(border=True):
            st.markdown("#### 📈 Missing Skills Roadmap")
            st.caption("Follow a 4-phase step-by-step career and project roadmap to eliminate resume gaps.")
            if st.button("View Career Roadmap", use_container_width=True):
                st.session_state["current_page"] = "roadmap"
                st.rerun()

    st.markdown("---")

    # ==================== TOP NEARBY & MATCHING JOBS ====================
    st.subheader(f"📍 Curated Top Matches Near {loc_str}")
    if skill_matches:
        for item in skill_matches[:4]:
            job = item["job"]
            matched_skills = item["matched_skills"]
            score = item["total_score"]
            is_local = item["is_local"]

            skills_html = "".join([f'<span class="skill-badge skill-badge-matched">✓ {s}</span>' for s in matched_skills[:5]])
            loc_badge = "📍 City/State Match" if is_local else "🌐 Remote / Worldwide"

            st.markdown(f"""
            <div class="job-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div class="job-title">{job['title']}</div>
                        <div class="job-company">{job['company']} &nbsp;•&nbsp; 📍 {job['city']}, {job['state']} ({job['country']})</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 13px;">
                            {score}% Match
                        </span>
                        <div style="font-size: 11px; color: #94A3B8; margin-top: 3px;">{loc_badge}</div>
                    </div>
                </div>
                <div class="job-meta">
                    <span>💰 {job['salary_range']}</span>
                    <span>💼 {job['job_type']}</span>
                    <span>🎓 {job['experience_required']}</span>
                </div>
                <div style="margin-top: 8px;">
                    <div style="font-size: 11.5px; font-weight: 600; color: #94A3B8; margin-bottom: 4px;">Matched Skills:</div>
                    {skills_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No immediate local matches found yet. Try updating your skills in your Profile to broaden matching opportunities!")
