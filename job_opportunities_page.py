"""
HireLens AI - Global Job Opportunities & Interactive World Map
Ultra-fast, mobile-responsive, 3D pydeck & plotly world mapping.
Automatically tailors, ranks, and filters job openings according to the candidate's attached resume.
"""
import streamlit as st
import pydeck as pdk
import plotly.graph_objects as go
import json
import re

try:
    from database.db import get_all_jobs, insert_job, get_user_resumes, create_notification
    from database.seed_data import WORLD_CITIES
    from core.notification_engine import calculate_skill_match, broadcast_job_to_candidates
    from core.ats_engine import extract_skills_from_text, extract_text_from_pdf, analyze_resume_ats
    from core.dataset_loader import DatasetEngine
except ModuleNotFoundError:
    from db import get_all_jobs, insert_job, get_user_resumes, create_notification
    from seed_data import WORLD_CITIES
    from notification_engine import calculate_skill_match, broadcast_job_to_candidates
    from ats_engine import extract_skills_from_text, extract_text_from_pdf, analyze_resume_ats
    from dataset_loader import DatasetEngine

from config import KAGGLE_CATEGORIES

def compute_job_resume_fit(job: dict, resume_skills: list[str], desired_category: str, user_city: str = "", user_state: str = "") -> dict:
    """Computes precision alignment between a job opening and candidate's attached resume."""
    req_skills_raw = job.get("required_skills", "")
    j_skills = [s.strip().lower() for s in re.split(r'[,|;/]', req_skills_raw) if s.strip()]
    
    r_skills_clean = [s.strip().lower() for s in resume_skills if s.strip()]
    
    matched = []
    missing = []
    
    for js in j_skills:
        found = False
        j_words = set(re.findall(r'[a-z0-9#+]+', js))
        for rs in r_skills_clean:
            if rs == js or rs in js or js in rs:
                matched.append(js)
                found = True
                break
            # Word-stem match (e.g. strategy/strategic, market/marketing, lead/leadership, manage/management)
            r_words = set(re.findall(r'[a-z0-9#+]+', rs))
            for rw in r_words:
                if len(rw) >= 4 and any(rw[:5] in jw for jw in j_words if len(jw) >= 4):
                    matched.append(js)
                    found = True
                    break
            if found:
                break
        if not found:
            missing.append(js)
            
    # Skill overlap percentage
    raw_skill_pct = (len(matched) / len(j_skills) * 100.0) if j_skills else 50.0
    
    # Category match bonus
    cat_match = bool(desired_category and job.get("category", "").upper().strip() == desired_category.upper().strip())
    
    # Location match bonus
    loc_match = False
    j_city = (job.get("city") or "").lower().strip()
    j_state = (job.get("state") or "").lower().strip()
    if user_city and (user_city.lower() in j_city or j_city in user_city.lower()):
        loc_match = True
    elif user_state and (user_state.lower() in j_state or j_state in user_state.lower()):
        loc_match = True
    elif job.get("job_type") == "Remote":
        loc_match = True
        
    # Weighted composite score: 55% skills + 35% category alignment + 10% location / remote
    composite = (raw_skill_pct * 0.55) + (35.0 if cat_match else 0.0) + (10.0 if loc_match else 0.0)
    composite = min(98.5, max(5.0, round(composite, 1)))
    
    return {
        "score": composite,
        "raw_skill_pct": round(raw_skill_pct, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "category_match": cat_match,
        "is_local": loc_match
    }

def render_job_opportunities():
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">
            🗺️ Job Opportunities & Interactive World Map
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 13.5px;">
            Discover career opportunities nearby and worldwide automatically tailored to your <strong>attached resume</strong> and <strong>desired domain</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    user_city = user.get("city", "")
    user_state = user.get("state", "")

    # ==================== DETECT ATTACHED RESUME CONTEXT ====================
    ats_analysis = st.session_state.get("latest_ats_analysis", {})
    analyzed_cat = st.session_state.get("analyzed_category") or ats_analysis.get("target_category") or ats_analysis.get("predicted_category")
    analyzed_text = st.session_state.get("analyzed_resume_text", "")
    
    # If no analysis in session, check saved user resumes in SQLite database
    if not ats_analysis and user and "id" in user:
        try:
            saved_resumes = get_user_resumes(user["id"])
            if saved_resumes:
                latest_saved = saved_resumes[0]
                analyzed_cat = latest_saved[5] or user.get("target_category", "INFORMATION-TECHNOLOGY")
                try:
                    r_data = json.loads(latest_saved[3])
                    analyzed_text = r_data.get("text", "")
                except Exception:
                    analyzed_text = ""
        except Exception:
            pass

    # Extract Active Candidate Skills from Attached Resume
    resume_skills_list = []
    if ats_analysis and "candidate_skills" in ats_analysis and ats_analysis["candidate_skills"]:
        resume_skills_list = ats_analysis["candidate_skills"]
    elif analyzed_text:
        resume_skills_list = extract_skills_from_text(analyzed_text)
    elif user.get("skills"):
        resume_skills_list = [s.strip().lower() for s in user.get("skills", "").split(",") if s.strip()]

    desired_category = analyzed_cat or user.get("target_category", "INFORMATION-TECHNOLOGY")

    # ==================== ATTACHED RESUME HERO CARD ====================
    has_active_resume = bool(resume_skills_list or analyzed_text or ats_analysis)
    
    if has_active_resume:
        skills_preview = ", ".join(resume_skills_list[:8])
        if len(resume_skills_list) > 8:
            skills_preview += f" (+{len(resume_skills_list)-8} more)"
            
        score_pill = ""
        if ats_analysis and "overall_score" in ats_analysis:
            score_pill = f"<span style='color: #6EE7B7; background: rgba(16,185,129,0.25); border: 1px solid rgba(16,185,129,0.4); padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700;'>ATS Score: {ats_analysis['overall_score']}%</span>"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.3) 0%, rgba(15, 23, 42, 0.6) 100%); border: 1px solid rgba(59, 130, 246, 0.35); border-left: 5px solid #3B82F6; border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 8px 24px -6px rgba(0,0,0,0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <span style="font-size: 15px; font-weight: 800; color: #FFFFFF;">🎯 Active Resume Attached:</span>
                        <span style="color: #93C5FD; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59,130,246,0.35); padding: 2px 10px; border-radius: 12px; font-size: 12.5px; font-weight: 700;">{desired_category}</span>
                        {score_pill}
                    </div>
                    <div style="color: #CBD5E1; font-size: 12.5px; margin-top: 6px; line-height: 1.4;">
                        <strong style="color:#94A3B8;">Matching Skills from Resume ({len(resume_skills_list)}):</strong> {skills_preview or 'Universal domain proficiencies'}
                    </div>
                </div>
                <div>
                    <span style="color: #6EE7B7; font-size: 12px; font-weight: 700; background: rgba(16,185,129,0.15); padding: 4px 10px; border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">
                        ⚡ Sorted by Resume Fit
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Attach or upload your resume below to automatically tailor, filter, and score all 121+ job opportunities worldwide against your qualifications!")

    # Collapsible Resume Attacher / Updater
    with st.expander("📎 Attach or Change Resume for Real-Time Job Matching", expanded=(not has_active_resume)):
        st.write("Upload a PDF or paste text to instantly recalculate precision match percentages and re-rank all global openings:")
        up_col1, up_col2 = st.columns([1, 1])
        with up_col1:
            job_up_file = st.file_uploader("Upload Resume (.pdf or .txt)", type=["pdf", "txt"], key="job_page_uploader")
        with up_col2:
            job_up_text = st.text_area("Or Paste Resume Text", height=100, placeholder="Paste resume text here to rank jobs by skills and field...", key="job_page_paste")
            
        if st.button("⚡ Recalculate Job Matching", key="btn_recalc_jobs", type="primary"):
            new_text = ""
            if job_up_file:
                if job_up_file.name.endswith(".pdf"):
                    new_text = extract_text_from_pdf(job_up_file.read())
                else:
                    new_text = job_up_file.read().decode("utf-8", errors="ignore")
            elif job_up_text:
                new_text = job_up_text.strip()
                
            if new_text and len(new_text.strip()) > 30:
                pred_c, _ = DatasetEngine.get_instance().predict_category(new_text)
                res = analyze_resume_ats(new_text, target_category=pred_c)
                st.session_state["latest_ats_analysis"] = res
                st.session_state["analyzed_resume_text"] = new_text
                st.session_state["analyzed_category"] = pred_c
                st.session_state["forced_target_cat"] = pred_c
                st.success(f"Attached resume analyzed! Tailoring jobs to **{pred_c}**.")
                st.rerun()

    # ==================== QUICK CITY CHIPS ====================
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

    # ==================== FILTER BAR ====================
    with st.container(border=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.2, 1.2, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search Keyword or Role", placeholder="e.g. Marketing, Manager, Python, Analyst")
        with f_col2:
            resume_choice_label = f"🎯 Matches My Resume ({desired_category})"
            cat_options = [resume_choice_label, "🌐 All 24 Domains"] + KAGGLE_CATEGORIES
            selected_cat_raw = st.selectbox("Category Filter", cat_options, index=0)
            
            if selected_cat_raw == resume_choice_label:
                selected_cat = desired_category
            elif selected_cat_raw == "🌐 All 24 Domains":
                selected_cat = "All"
            else:
                selected_cat = selected_cat_raw

        with f_col3:
            job_types = ["All", "Full-time", "Remote", "Hybrid", "On-site"]
            selected_type = st.selectbox("Work Type", job_types, index=0)
        with f_col4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            filter_nearby = st.checkbox(f"📍 Near Me ({user_city or 'My City'})", value=(st.session_state["selected_quick_city"] == user_city and bool(user_city)))

    # Fetch jobs from database
    city_filter = None
    if st.session_state["selected_quick_city"] != "All":
        city_filter = st.session_state["selected_quick_city"]

    raw_jobs = get_all_jobs(
        category=selected_cat if selected_cat != "All" else None,
        city=city_filter,
        search=search_query if search_query else None,
        limit=300
    )

    if selected_type != "All":
        raw_jobs = [j for j in raw_jobs if j["job_type"] == selected_type]

    if filter_nearby and user_city:
        raw_jobs = [
            j for j in raw_jobs 
            if (user_city.lower() in j["city"].lower()) or 
               (user_state and user_state.lower() in j["state"].lower()) or 
               (j["job_type"] == "Remote")
        ]

    # Compute precision fit for every job and sort by score descending
    scored_jobs = []
    for j in raw_jobs:
        fit = compute_job_resume_fit(j, resume_skills_list, desired_category, user_city, user_state)
        scored_jobs.append({
            "job": j,
            "fit": fit
        })

    # Sort so top matching positions appear at the top
    scored_jobs.sort(key=lambda x: x["fit"]["score"], reverse=True)

    st.markdown(f"**Showing {len(scored_jobs)} openings aligned with your resume:**")

    # ==================== INTERACTIVE WORLD MAP ====================
    tab_deck, tab_plotly = st.tabs(["🌐 3D Pydeck Interactive Map", "🗺️ Plotly Global View"])

    map_data = []
    for item in scored_jobs:
        j = item["job"]
        fit = item["fit"]
        if j.get("latitude") and j.get("longitude"):
            score = fit["score"]
            if score >= 60:
                color = [16, 185, 129, 230] # Glowing Green
            elif score >= 35:
                color = [59, 130, 246, 210] # Blue
            else:
                color = [148, 163, 184, 180] # Slate

            matched_preview = ", ".join(fit["matched_skills"][:3]) if fit["matched_skills"] else "Domain Alignment"

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
                "match": f"{score}% Match",
                "matched_preview": matched_preview,
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
                            "🎯 <b>{match} with your Resume</b><br/>"
                            "🏷️ {category} &nbsp;•&nbsp; 💼 {type}<br/>"
                            "✓ {matched_preview}",
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
            texts = [f"<b>{d['title']}</b><br>{d['company']}<br>{d['city']}, {d['state']}<br>{d['salary']}<br>🎯 {d['match']} with Resume" for d in map_data]

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
        st.subheader("📋 Available Positions (Ranked by Resume Fit)")
        if not scored_jobs:
            st.warning("No jobs matched your filters. Try selecting 'All' categories or removing keywords.")
        else:
            for item in scored_jobs[:20]:
                job = item["job"]
                fit = item["fit"]
                match_score = fit["score"]
                
                is_local = fit["is_local"]
                loc_badge = "📍 City / Regional Match" if is_local else "🌐 Worldwide Opening"
                
                if match_score >= 65:
                    score_badge_style = "background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.4);"
                elif match_score >= 40:
                    score_badge_style = "background: rgba(59, 130, 246, 0.2); color: #93C5FD; border: 1px solid rgba(59,130,246,0.4);"
                else:
                    score_badge_style = "background: rgba(148, 163, 184, 0.15); color: #CBD5E1; border: 1px solid rgba(148,163,184,0.3);"

                # Format matched vs missing skills
                matched_tags = ""
                if fit["matched_skills"]:
                    matched_tags = "".join([f'<span class="skill-badge skill-badge-matched"><span style="color:#34D399;font-weight:700;margin-right:4px;">✓</span>{s}</span>' for s in fit["matched_skills"][:5]])
                else:
                    matched_tags = "<span style='color: #94A3B8; font-size: 11.5px;'>Domain aligned</span>"

                missing_tags = ""
                if fit["missing_skills"]:
                    missing_tags = "".join([f'<span class="skill-badge skill-badge-missing"><span style="color:#F87171;font-weight:700;margin-right:4px;">✕</span>{s}</span>' for s in fit["missing_skills"][:3]])

                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div class="job-title">{job['title']}</div>
                            <div class="job-company">{job['company']} &nbsp;•&nbsp; 📍 {job['city']}, {job['state']} ({job['country']})</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="{score_badge_style} padding: 5px 12px; border-radius: 10px; font-weight: 800; font-size: 13.5px; display: inline-block;">
                                🔥 {match_score}% Match with Resume
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
                    <div style="font-size: 12.5px; color: #CBD5E1; margin: 8px 0; line-height: 1.45;">
                        {job['description']}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px;">
                        <strong style="color: #6EE7B7;">Matched Skills:</strong> {matched_tags}
                    </div>
                    {f'<div style="margin-top: 4px; font-size: 12px;"><strong style="color: #FCA5A5;">Gaps:</strong> {missing_tags}</div>' if missing_tags else ''}
                </div>
                """, unsafe_allow_html=True)

                btn_apply_label = f"⚡ One-Click Apply with {desired_category} Resume"
                if st.button(btn_apply_label, key=f"apply_{job['id']}", type="primary" if match_score >= 60 else "secondary", use_container_width=True):
                    if user and "id" in user:
                        create_notification(
                            user_id=user["id"],
                            title=f"Application Submitted: {job['title']}",
                            message=f"Your attached resume was submitted to {job['company']} for {job['title']} ({job['city']}, {job['country']}). Match: {match_score}%. Recruiter notified!",
                            job_id=job["id"]
                        )
                    st.toast(f"🎉 Application submitted for {job['title']} at {job['company']} with your {desired_category} resume!", icon="✅")

    # ==================== RECRUITER POSTING TOOL ====================
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
