"""
HireLens AI - Next-Gen Resume Intelligence & Career Ecosystem
Main Application Entry Point (Ultra-Fast, Mobile-Responsive & Cloud-Resilient)
"""
import os
import sys

# Ensure repository root is on sys.path for cloud deployment (Linux / Streamlit Cloud)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="HireLens AI - Resume Intelligence & Career Hub",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load custom responsive CSS (supports both assets/style.css and style.css in root)
for css_candidate in [os.path.join(ROOT_DIR, "assets", "style.css"), os.path.join(ROOT_DIR, "style.css")]:
    if os.path.exists(css_candidate):
        with open(css_candidate, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        break

# Hybrid imports (supports both folder package structure and flat GitHub upload structure)
try:
    from database.seed_data import seed_database
    from database.db import get_user_notifications
except ModuleNotFoundError:
    from seed_data import seed_database
    from db import get_user_notifications

try:
    from pages_modules.login_page import render_login_page
    from pages_modules.dashboard_page import render_dashboard
    from pages_modules.ats_analyzer_page import render_ats_analyzer
    from pages_modules.roadmap_page import render_roadmap_page
    from pages_modules.resume_maker_page import render_resume_maker
    from pages_modules.job_opportunities_page import render_job_opportunities
    from pages_modules.profile_page import render_profile_page
    from pages_modules.dataset_explorer_page import render_dataset_explorer
except ModuleNotFoundError:
    from login_page import render_login_page
    from dashboard_page import render_dashboard
    from ats_analyzer_page import render_ats_analyzer
    from roadmap_page import render_roadmap_page
    from resume_maker_page import render_resume_maker
    from job_opportunities_page import render_job_opportunities
    from profile_page import render_profile_page
    from dataset_explorer_page import render_dataset_explorer

# Bootstrap database and cache on startup ONLY ONCE (avoids slow per-rerun queries!)
@st.cache_resource(show_spinner=False)
def bootstrap_system():
    seed_database()
    return True

bootstrap_system()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"

def main():
    if not st.session_state["logged_in"] or not st.session_state["user"]:
        render_login_page()
        return

    user = st.session_state["user"]
    
    # Efficient notification caching: only query when unread_count is not cached or marked dirty
    if "unread_count" not in st.session_state or st.session_state.get("refresh_notifs", False):
        try:
            notifs = get_user_notifications(user["id"], limit=5)
            st.session_state["unread_count"] = sum(1 for n in notifs if not n["is_read"])
            st.session_state["refresh_notifs"] = False
        except Exception:
            st.session_state["unread_count"] = 0
    unread_count = st.session_state.get("unread_count", 0)

    # Define Navigation Structure
    notif_badge = f" 🔥 ({unread_count})" if unread_count > 0 else ""
    pages = {
        "dashboard": f"🏠 Dashboard{notif_badge}",
        "ats_analyzer": "🎯 AI ATS Analyzer",
        "roadmap": "📈 Missing Values Roadmap",
        "resume_maker": "📝 AI Resume Maker (Blank)",
        "job_opportunities": "🗺️ Job Opportunities & Map",
        "profile": "👤 Profile & Alerts",
        "dataset_explorer": "📊 Kaggle Dataset Explorer"
    }

    page_keys = list(pages.keys())
    current_key = st.session_state.get("current_page", "dashboard")
    default_index = page_keys.index(current_key) if current_key in page_keys else 0

    # ==================== TOP QUICK-NAV BAR (Mobile & Laptop Fast Switching) ====================
    top_nav_items = [
        ("dashboard", "🏠", "Dashboard"),
        ("ats_analyzer", "🎯", "ATS Audit"),
        ("roadmap", "📈", "Roadmap"),
        ("resume_maker", "📝", "Resume Maker"),
        ("job_opportunities", "🗺️", "Job Map"),
        ("profile", "👤", "Profile")
    ]
    
    st.markdown('<div class="top-nav-bar">', unsafe_allow_html=True)
    t_cols = st.columns(len(top_nav_items))
    for idx, (p_key, icon, label) in enumerate(top_nav_items):
        with t_cols[idx]:
            is_active = (current_key == p_key)
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon} {label}", key=f"tnav_{p_key}", type=btn_type, use_container_width=True):
                if current_key != p_key:
                    st.session_state["current_page"] = p_key
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ==================== SIDEBAR NAVIGATION (Desktop & Tablet) ====================
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0 14px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🎯</span>
                <div>
                    <div style="font-size: 19px; font-weight: 800; color: #60A5FA; letter-spacing: -0.3px;">HireLens AI</div>
                    <div style="font-size: 11px; color: #94A3B8;">Career & Resume Intelligence</div>
                </div>
            </div>
            <div style="margin-top: 12px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.05); padding: 8px 12px; border-radius: 10px;">
                <div style="font-size: 13px; font-weight: 700; color: #F8FAFC;">{user.get('full_name', 'User')}</div>
                <div style="font-size: 11px; color: #94A3B8;">📍 {user.get('city', 'City')}, {user.get('state', 'State')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected_label = st.radio(
            "Navigate",
            options=list(pages.values()),
            index=default_index,
            label_visibility="collapsed"
        )

        for k, v in pages.items():
            if v == selected_label and k != current_key:
                st.session_state["current_page"] = k
                st.rerun()
                break

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["current_page"] = "dashboard"
            st.rerun()

    # ==================== ROUTE TO ACTIVE PAGE ====================
    page = st.session_state["current_page"]
    if page == "dashboard":
        render_dashboard()
    elif page == "ats_analyzer":
        render_ats_analyzer()
    elif page == "roadmap":
        render_roadmap_page()
    elif page == "resume_maker":
        render_resume_maker()
    elif page == "job_opportunities":
        render_job_opportunities()
    elif page == "profile":
        render_profile_page()
    elif page == "dataset_explorer":
        render_dataset_explorer()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
