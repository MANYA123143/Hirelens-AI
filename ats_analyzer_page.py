"""
HireLens AI - AI Resume Analysis & ATS Checker Page
High-speed, mobile-responsive, visual gauge & radar scoring engine.
Evaluates both Technical and Non-Technical / Soft / Leadership skills.
"""
import streamlit as st
import plotly.graph_objects as go

try:
    from core.ats_engine import analyze_resume_ats, extract_text_from_pdf
    from core.dataset_loader import DatasetEngine
    from core.skills_taxonomy import SKILL_CATEGORIES
    from database.db import save_user_resume
except ModuleNotFoundError:
    from ats_engine import analyze_resume_ats, extract_text_from_pdf
    from dataset_loader import DatasetEngine
    from skills_taxonomy import SKILL_CATEGORIES
    from db import save_user_resume

from config import KAGGLE_CATEGORIES

def render_ats_analyzer():
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">
            🎯 AI Resume Analysis & ATS Checker
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 13.5px;">
            Benchmark your resume against 2,484 profiles from the Kaggle Resume dataset across all <strong>Technical</strong> and <strong>Non-Technical / Soft Skills</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    dataset_engine = DatasetEngine.get_instance()
    user = st.session_state.get("user", {})

    preloaded_text = st.session_state.get("resume_to_analyze", "")

    col_input_left, col_input_right = st.columns([1.1, 0.9])

    with col_input_left:
        st.subheader("1. Resume Source")
        input_mode = st.radio("Choose Input Method", ["📄 Upload PDF / TXT", "✍️ Paste Text", "📂 Kaggle Sample"], horizontal=True)

        resume_text = ""
        if input_mode == "📄 Upload PDF / TXT":
            uploaded_file = st.file_uploader("Upload resume (.pdf or .txt)", type=["pdf", "txt"])
            if uploaded_file is not None:
                if uploaded_file.name.endswith(".pdf"):
                    with st.spinner("Extracting text from PDF..."):
                        resume_text = extract_text_from_pdf(uploaded_file.read())
                else:
                    resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
                st.success(f"Loaded '{uploaded_file.name}' ({len(resume_text.split())} words)")
        
        elif input_mode == "✍️ Paste Text":
            default_val = preloaded_text if preloaded_text else ""
            resume_text = st.text_area(
                "Paste Resume Text Here",
                value=default_val,
                height=220,
                placeholder="Paste your full resume text including Summary, Skills, Experience, Education, and Projects..."
            )

        else: # Load Kaggle Dataset Sample
            selected_cat = st.selectbox("Select Kaggle Category Benchmark", KAGGLE_CATEGORIES, index=0)
            sample_txt = dataset_engine.get_sample_resume(selected_cat)
            st.info(f"Loaded sample resume for **{selected_cat}** from `Divyaamith/Kaggle-Resume`.")
            resume_text = st.text_area("Sample Resume Content", value=sample_txt[:2500], height=200)

    with col_input_right:
        st.subheader("2. Target Role & Category")
        
        default_cat_index = 0
        user_cat = user.get("target_category", "INFORMATION-TECHNOLOGY")
        if user_cat in KAGGLE_CATEGORIES:
            default_cat_index = KAGGLE_CATEGORIES.index(user_cat)

        target_category = st.selectbox(
            "Target Category (from Kaggle Dataset)",
            KAGGLE_CATEGORIES,
            index=default_cat_index
        )

        job_desc = st.text_area(
            "Job Description (Optional for custom matching)",
            height=140,
            placeholder="Paste target job description to compute precision technical and soft skill match..."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        run_analysis = st.button("⚡ Run Full AI ATS Audit", type="primary", use_container_width=True)

    if run_analysis:
        if not resume_text or len(resume_text.strip()) < 40:
            st.error("Please supply a resume with at least 40 words to analyze.")
            return

        with st.spinner("Auditing technical skills, soft skills, leadership, action verbs, and ATS compatibility..."):
            result = analyze_resume_ats(
                resume_text=resume_text,
                target_category=target_category,
                job_description=job_desc
            )
            st.session_state["latest_ats_analysis"] = result
            st.session_state["analyzed_resume_text"] = resume_text
            st.session_state["analyzed_category"] = target_category

            if result["overall_score"] >= 80:
                st.balloons()

            if user:
                save_user_resume(
                    user_id=user["id"],
                    resume_name=f"Resume Scan - {target_category}",
                    resume_data_dict={"text": resume_text[:1000], "overall_score": result["overall_score"]},
                    ats_score=result["overall_score"],
                    category=target_category
                )

    # ==================== RENDER ANALYSIS RESULTS ====================
    if "latest_ats_analysis" in st.session_state:
        res = st.session_state["latest_ats_analysis"]
        overall = res["overall_score"]
        grade = res["grade"]
        color = res["badge_color"]
        sub = res["sub_scores"]

        st.markdown("---")
        st.markdown("### 📊 Interactive ATS Audit Breakdown")

        # Visual Row: Gauge + Radar Chart
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"ATS Score: Grade {grade}", 'font': {'size': 20, 'color': '#FFFFFF'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                    'bar': {'color': color},
                    'bgcolor': "#1E293B",
                    'borderwidth': 1,
                    'bordercolor': "#334155",
                    'steps': [
                        {'range': [0, 55], 'color': 'rgba(239, 68, 68, 0.2)'},
                        {'range': [55, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                    ],
                    'threshold': {
                        'line': {'color': "#60A5FA", 'width': 3},
                        'thickness': 0.75,
                        'value': 85
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#F8FAFC"),
                height=260,
                margin=dict(l=20, r=20, t=40, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_g2:
            # 6-Axis Multi-Dimensional Radar Chart (Technical + Soft + Management)
            categories_radar = ['Technical Skills', 'Soft Skills', 'Leadership & Ops', 'Problem Solving', 'ATS Sections', 'Impact Metrics']
            
            cand_by_cat = res.get("candidate_by_category", {})
            tech_val = sub.get('technical_match', 70.0)
            soft_val = sub.get('soft_match', 70.0)
            lead_val = min(100.0, len(cand_by_cat.get("Leadership & Management", [])) * 25.0 + 30.0)
            prob_val = min(100.0, len(cand_by_cat.get("Analytical & Problem Solving", [])) * 25.0 + 30.0)
            sec_val = sub['section_completeness']
            imp_val = sub['impact_metrics']

            values_radar = [tech_val, soft_val, lead_val, prob_val, sec_val, imp_val]
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values_radar,
                theta=categories_radar,
                fill='toself',
                fillcolor='rgba(59, 130, 246, 0.3)',
                line=dict(color='#3B82F6', width=2)
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#94A3B8')),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#F8FAFC"),
                showlegend=False,
                height=260,
                margin=dict(l=35, r=35, t=30, b=30)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # 4 Sub-score metrics
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("Technical Fit", f"{sub.get('technical_match', sub['skill_match'])}%", help="Match on hard technical & software skills")
        with sc2:
            st.metric("Soft & Leadership Fit", f"{sub.get('soft_match', sub['skill_match'])}%", help="Match on communication, teamwork, and management skills")
        with sc3:
            st.metric("Section Completeness", f"{sub['section_completeness']}%", help="Audit of 6 essential ATS resume sections")
        with sc4:
            st.metric("Action & Impact Metrics", f"{sub['impact_metrics']}%", help="Power action verbs and measurable quantifiable metrics")

        st.markdown("<br>", unsafe_allow_html=True)

        # Categorized Skills Tabs
        tab_skills_all, tab_sections, tab_verbs, tab_recs = st.tabs([
            "🎯 Skills Breakdown (Technical + Non-Technical)",
            "📋 Sections Audit",
            "⚡ Action Verbs & Metrics",
            "💡 High-Impact Recommendations"
        ])

        with tab_skills_all:
            matched_by_cat = res.get("matched_by_category", {})
            missing_by_cat = res.get("missing_by_category", {})

            col_sk1, col_sk2 = st.columns(2)
            with col_sk1:
                st.markdown("#### ✅ Matched Skills in Resume")
                if not matched_by_cat:
                    st.warning("No explicit target skills detected.")
                else:
                    for cat_title, skill_list in matched_by_cat.items():
                        st.markdown(f"**{cat_title} ({len(skill_list)})**")
                        tags = "".join([f'<span class="skill-badge skill-badge-matched">✓ {s}</span>' for s in skill_list])
                        st.markdown(tags, unsafe_allow_html=True)

            with col_sk2:
                st.markdown("#### ❌ Missing Critical Skills (Gaps)")
                if not missing_by_cat:
                    st.success("All target skills matched!")
                else:
                    for cat_title, skill_list in missing_by_cat.items():
                        st.markdown(f"**{cat_title} ({len(skill_list)})**")
                        tags = "".join([f'<span class="skill-badge skill-badge-missing">✗ {s}</span>' for s in skill_list])
                        st.markdown(tags, unsafe_allow_html=True)

        with tab_sections:
            st.markdown("#### 📋 Essential Resume Sections Check")
            sec_cols = st.columns(3)
            for idx, (section, is_present) in enumerate(res["sections_audit"].items()):
                c = sec_cols[idx % 3]
                icon = "✅" if is_present else "❌"
                status_text = "Detected" if is_present else "Missing / Not Found"
                color_txt = "#34D399" if is_present else "#F87171"
                c.markdown(f"**{icon} {section}**  \n<span style='color:{color_txt}; font-size:12px;'>{status_text}</span>", unsafe_allow_html=True)

        with tab_verbs:
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.markdown(f"#### 🚀 Action Verbs Detected ({len(res['found_verbs'])})")
                if res["found_verbs"]:
                    st.write(", ".join([v.title() for v in res["found_verbs"]]))
                else:
                    st.warning("No strong action verbs found. Replace passive phrases with verbs like 'Spearheaded', 'Optimized', 'Engineered', 'Negotiated'.")

            with col_v2:
                st.markdown(f"#### 📈 Measurable Metrics Found ({len(res['metrics_found'])})")
                if res["metrics_found"]:
                    for m in res["metrics_found"]:
                        st.markdown(f"• `{m}`")
                else:
                    st.warning("No measurable metrics detected. Include percentages (%), dollar amounts ($), or volume numbers.")

        with tab_recs:
            st.markdown("#### 💡 Tailored Action Plan")
            for rec in res["recommendations"]:
                st.markdown(f"- {rec}")

        # CTA for Roadmap
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🎯 **Next Step:** We have generated a step-by-step career and project roadmap to eliminate the missing technical and soft skills detected in this analysis!")
        if st.button("🗺️ View Personalized Missing Values Roadmap", type="primary", use_container_width=True):
            st.session_state["current_page"] = "roadmap"
            st.rerun()
