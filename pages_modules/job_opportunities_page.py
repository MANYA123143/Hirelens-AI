"""
HireLens AI - Global Job Opportunities & Interactive World Map
Ultra-fast, mobile-responsive, 3D pydeck & plotly world mapping with 1-tap proximity filters.
"""
import streamlit as st
import pydeck as pdk
import plotly.graph_objects as go
from database.db import get_all_jobs, insert_job
from database.seed_data import WORLD_CITIES
from core.notification_engine import calculate_skill_match, broadcast_job_to_candidates
from config import KAGGLE_CATEGORIES

def render_job_opportunities():
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">
            🗺️ Job Opportunities & Interactive World Map
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 13.5px;">
            Discover career opportunities nearby in your city and state, or navigate global hiring hotspots across the world map.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    user_city = user.get("city", "")
    user_state = user.get("state", "")
    user_skills = user.get("skills", "")

    # Quick City Chips for Mobile & Desktop
    st.write("**Quick City Filters:**")
    quick_cities = ["All", user_city if user_city else "Bengaluru", "San Francisco", "London", "New York", "Berlin", "Dubai", "Singapore"]
    qc_cols = st.columns(len(quick_cities))
    
    if "selected_quick_city" not in st.session_state:
        st.session_state["selected_quick_city"] = "All"

    for idx, qc in enumerate(quick_cities):
        with qc_cols[idx]:
            is_active = (st.session_state["selected_quick_city"] == qc)
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"📍 {qc}", key=f"qc_{idx}_{qc}", type=btn_type, use_container_width=True):
                st.session_state["selected_quick_city"] = qc
                st.rerun()

    # Filter Bar
    with st.container(border=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.2, 1, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search Keyword or Skill", placeholder="e.g. Python, Machine Learning, Analyst")
        with f_col2:
            cat_options = ["All"] + KAGGLE_CATEGORIES
            selected_cat = st.selectbox("Category", cat_options, index=0)
        with f_col3:
            job_types = ["All", "Full-time", "Remote", "Hybrid", "On-site"]
            selected_type = st.selectbox("Work Type", job_types, index=0)
        with f_col4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            filter_nearby = st.checkbox(f"📍 Near Me ({user_city or 'My City'})", value=(st.session_state["selected_quick_city"] == user_city and bool(user_city)))

    # Fetch jobs
    city_filter = None
    if st.session_state["selected_quick_city"] != "All":
        city_filter = st.session_state["selected_quick_city"]

    all_jobs = get_all_jobs(
        category=selected_cat if selected_cat != "All" else None,
        city=city_filter,
        search=search_query if search_query else None,
        limit=300
    )

    if selected_type != "All":
        all_jobs = [j for j in all_jobs if j["job_type"] == selected_type]

    if filter_nearby and user_city:
        all_jobs = [
            j for j in all_jobs 
            if (user_city.lower() in j["city"].lower()) or 
               (user_state and user_state.lower() in j["state"].lower()) or 
               (j["job_type"] == "Remote")
        ]

    st.markdown(f"**Showing {len(all_jobs)} openings:**")

    # ==================== INTERACTIVE WORLD MAP ====================
    tab_deck, tab_plotly = st.tabs(["🌐 3D Pydeck Interactive Map", "🗺️ Plotly Global View"])

    map_data = []
    for j in all_jobs:
        if j.get("latitude") and j.get("longitude"):
            pct, _ = calculate_skill_match(user_skills, j.get("required_skills", ""))
            color = [16, 185, 129, 210] if pct >= 50 else [59, 130, 246, 200]
            map_data.append({
                "title": j["title"],
                "company": j["company"],
                "category": j["category"],
                "city": j["city"],
                "state": j["state"],
                "country": j["country"],
                "lat": float(j["latitude"]),
                "lon": float(j["longitude"]),
                "salary": j["salary_range"],
                "type": j["job_type"],
                "match": f"{pct}% Match",
                "color": color
            })

    with tab_deck:
        if map_data:
            center_lat, center_lon, zoom_lvl = 25.0, 10.0, 1.2
            if filter_nearby and user.get("latitude") and user.get("longitude") and user["latitude"] != 0:
                center_lat, center_lon, zoom_lvl = user["latitude"], user["longitude"], 9.0
            elif map_data:
                center_lat, center_lon = map_data[0]["lat"], map_data[0]["lon"]

            view_state = pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=zoom_lvl,
                pitch=30
            )

            scatterplot_layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position="[lon, lat]",
                get_color="color",
                get_radius=85000,
                radius_min_pixels=6,
                radius_max_pixels=25,
                pickable=True,
                auto_highlight=True
            )

            column_layer = pdk.Layer(
                "ColumnLayer",
                data=map_data,
                get_position="[lon, lat]",
                get_elevation=45000,
                elevation_scale=50,
                radius=40000,
                get_fill_color="color",
                pickable=True,
                auto_highlight=True
            )

            deck = pdk.Deck(
                layers=[scatterplot_layer, column_layer],
                initial_view_state=view_state,
                tooltip={
                    "html": "<b>{title}</b><br/>"
                            "🏢 {company}<br/>"
                            "📍 {city}, {state} ({country})<br/>"
                            "💰 {salary}<br/>"
                            "🏷️ {category} &nbsp;•&nbsp; <b>{match}</b>",
                    "style": {"backgroundColor": "#0F172A", "color": "#F8FAFC", "fontSize": "12px", "padding": "8px", "borderRadius": "8px"}
                },
                map_style="mapbox://styles/mapbox/dark-v10"
            )
            st.pydeck_chart(deck)
        else:
            st.info("No geospatial data matching the current filter.")

    with tab_plotly:
        if map_data:
            lats = [d["lat"] for d in map_data]
            lons = [d["lon"] for d in map_data]
            texts = [f"<b>{d['title']}</b><br>{d['company']}<br>{d['city']}, {d['state']}<br>{d['salary']}<br>{d['match']}" for d in map_data]

            fig = go.Figure(go.Scattergeo(
                lon=lons,
                lat=lats,
                text=texts,
                mode='markers',
                marker=dict(
                    size=10,
                    color='#3B82F6',
                    opacity=0.85,
                    line=dict(width=1, color='#FFFFFF')
                )
            ))
            fig.update_layout(
                geo=dict(
                    projection_type='natural earth',
                    showland=True,
                    landcolor='#1E293B',
                    bgcolor='#0F172A',
                    countrycolor='#334155',
                    coastlinecolor='#334155'
                ),
                paper_bgcolor='#0F172A',
                plot_bgcolor='#0F172A',
                margin=dict(l=0, r=0, t=10, b=10),
                height=420
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== JOB CARDS & RECRUITER TOOL ====================
    col_list, col_recruiter = st.columns([1.8, 1.2])

    with col_list:
        st.subheader("📋 Available Positions")
        if not all_jobs:
            st.warning("No jobs matched your filters. Try selecting 'All' categories or removing keywords.")
        else:
            for job in all_jobs[:15]:
                match_pct, matched_skills = calculate_skill_match(user_skills, job.get("required_skills", ""))
                
                is_local = False
                if user_city and user_city.lower() in job["city"].lower():
                    is_local = True
                elif user_state and user_state.lower() in job["state"].lower():
                    is_local = True

                loc_badge = "📍 City Match" if is_local else "🌐 Regional / Worldwide"
                score_badge_color = "#34D399" if match_pct >= 60 else ("#60A5FA" if match_pct >= 30 else "#94A3B8")

                skills_list = [s.strip() for s in job["required_skills"].split(",") if s.strip()]
                skills_tags = "".join([f'<span class="skill-badge">{s}</span>' for s in skills_list[:5]])

                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div class="job-title">{job['title']}</div>
                            <div class="job-company">{job['company']} &nbsp;•&nbsp; 📍 {job['city']}, {job['state']} ({job['country']})</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: rgba(59, 130, 246, 0.15); color: {score_badge_color}; border: 1px solid rgba(59,130,246,0.3); padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 13px;">
                                {match_pct}% Match
                            </span>
                            <div style="font-size: 11px; color: #94A3B8; margin-top: 3px;">{loc_badge}</div>
                        </div>
                    </div>
                    <div class="job-meta">
                        <span>💰 {job['salary_range']}</span>
                        <span>💼 {job['job_type']}</span>
                        <span>🎓 {job['experience_required']}</span>
                        <span>🏷️ {job['category']}</span>
                    </div>
                    <div style="font-size: 12.5px; color: #CBD5E1; margin: 8px 0; line-height: 1.4;">
                        {job['description']}
                    </div>
                    <div>{skills_tags}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🚀 One-Click Apply", key=f"apply_{job['id']}", use_container_width=True):
                    st.toast(f"✅ Application submitted for {job['title']} at {job['company']}!", icon="🎉")

    # Recruiter Posting
    with col_recruiter:
        with st.container(border=True):
            st.markdown("#### 📢 Post New Job Requirement")
            st.caption("Recruiter Tool: Posting a job instantly scans candidate profiles and broadcasts real-time pop-up notification alerts!")

            with st.form("post_job_form"):
                p_title = st.text_input("Job Title *", placeholder="e.g. Senior AI Engineer")
                p_company = st.text_input("Company Name *", placeholder="e.g. Acme Tech Innovations")
                p_category = st.selectbox("Category (from Kaggle)", KAGGLE_CATEGORIES, index=KAGGLE_CATEGORIES.index("INFORMATION-TECHNOLOGY") if "INFORMATION-TECHNOLOGY" in KAGGLE_CATEGORIES else 0)
                
                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    p_city = st.text_input("City *", placeholder="e.g. Bengaluru")
                    p_state = st.text_input("State *", placeholder="e.g. Karnataka")
                with c_p2:
                    p_country = st.text_input("Country *", placeholder="e.g. India")
                    p_type = st.selectbox("Arrangement", ["Full-time", "Remote", "Hybrid", "On-site"])

                p_salary = st.text_input("Salary Range", placeholder="e.g. $140,000 - $180,000 or ₹22,00,000")
                p_exp = st.selectbox("Experience Level", ["Fresher / Entry (0-1 yrs)", "Junior (1-3 yrs)", "Mid-Level (3-5 yrs)", "Senior (5+ yrs)"])
                p_skills = st.text_area("Required Skills (comma-separated) *", placeholder="e.g. Python, PyTorch, React, Docker, SQL")
                p_desc = st.text_area("Job Summary", placeholder="Brief description of primary duties...")

                submit_job = st.form_submit_button("🚀 Publish & Broadcast Alerts", type="primary", use_container_width=True)

                if submit_job:
                    if not (p_title and p_company and p_city and p_skills):
                        st.error("Please fill in title, company, city, and required skills.")
                    else:
                        coords = WORLD_CITIES.get((p_city.strip(), p_state.strip(), p_country.strip()), (25.0, 15.0))
                        new_job_id = insert_job(
                            title=p_title.strip(),
                            company=p_company.strip(),
                            category=p_category,
                            city=p_city.strip(),
                            state=p_state.strip(),
                            country=p_country.strip(),
                            lat=coords[0],
                            lon=coords[1],
                            salary_range=p_salary or "Competitive",
                            job_type=p_type,
                            experience_required=p_exp,
                            required_skills=p_skills.strip(),
                            description=p_desc.strip(),
                            source="Recruiter Direct"
                        )
                        alerts_sent = broadcast_job_to_candidates(new_job_id)
                        st.success(f"🎉 Job published! Real-time alerts dispatched to {alerts_sent} matching candidates.")
                        st.rerun()
