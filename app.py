"""
HireLens AI - Next-Gen Resume Intelligence & Career Ecosystem
Main Application Entry Point (Ultra-Fast & Mobile-Responsive)
"""
import os
import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="HireLens AI - Resume Intelligence & Career Hub",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load custom responsive CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Bootstrap database and cache on startup ONLY ONCE (avoids slow per-rerun queries!)
@st.cache_resource(show_spinner=False)
def bootstrap_system():
    from database.seed_data import seed_database
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

# Import Page Modules
from pages_modules.login_page import render_login_page
from pages_modules.dashboard_page import render_dashboard
from pages_modules.ats_analyzer_page import render_ats_analyzer
from pages_modules.roadmap_page import render_roadmap_page
from pages_modules.resume_maker_page import render_resume_maker
from pages_modules.job_opportunities_page import render_job_opportunities
from pages_modules.profile_page import render_profile_page
from pages_modules.dataset_explorer_page import render_dataset_explorer
from database.db import get_user_notifications

def main():
    # If not logged in, render authentication page
    if not st.session_state["logged_in"] or not st.session_state["user"]:
        render_login_page()
        return

    user = st.session_state["user"]
    notifications = get_user_notifications(user["id"], limit=5)
    unread_count = sum(1 for n in notifications if not n["is_read"])

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
            if v == selected_label:
                st.session_state["current_page"] = k
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
