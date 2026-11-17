"""
HireLens AI - Missing Values & Skills Career Roadmap Page
Interactive 4-phase step-by-step career and skills roadmap to bridge detected resume gaps.
"""
import streamlit as st
from core.roadmap_generator import generate_missing_values_roadmap
from core.ats_engine import analyze_resume_ats

def render_roadmap_page():
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">
            📈 Personalized Career & Skills Roadmap for Missing Values
        </h2>
        <p style="color: #94A3B8; margin: 0; font-size: 13.5px;">
            A structured, 4-phase career roadmap tailored to eliminate your missing skills, incomplete sections, and ATS gaps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    user_name = user.get("full_name", "Student Candidate")
    target_cat = user.get("target_category", "INFORMATION-TECHNOLOGY")

    ats_res = st.session_state.get("latest_ats_analysis")
    if not ats_res:
        st.info("💡 Run an ATS scan on your resume in the **ATS Analyzer** to personalize this roadmap to your exact document. Below is a roadmap based on your profile domain.")
        dummy_resume = f"Experienced candidate in {target_cat}. Background with fundamental tools and academic coursework."
        ats_res = analyze_resume_ats(dummy_resume, target_category=target_cat)

    roadmap = generate_missing_values_roadmap(
        ats_analysis_result=ats_res,
        candidate_name=user_name,
        target_category=target_cat
    )

    # Top Overview Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Current ATS Score", f"{roadmap['current_score']}%", delta=f"+{round(roadmap['target_score'] - roadmap['current_score'], 1)}% Target")
    with m2:
        st.metric("Target Benchmark", "95.0%", "Elite ATS Pass")
    with m3:
        st.metric("Missing Skills Gaps", f"{roadmap['missing_skills_count']} Skills", delta_color="inverse")
    with m4:
        st.metric("Estimated Timeline", "6 Weeks", "To Job-Readiness")

    st.markdown("<br>", unsafe_allow_html=True)

    if "roadmap_completed_tasks" not in st.session_state:
        st.session_state["roadmap_completed_tasks"] = set()

    total_tasks = 12
    completed_count = len(st.session_state["roadmap_completed_tasks"])
    progress_val = min(1.0, completed_count / total_tasks)
    
    st.write(f"**Roadmap Progress:** {int(progress_val * 100)}% ({completed_count} of {total_tasks} milestones completed)")
    st.progress(progress_val)

    if progress_val >= 1.0:
        st.success("🎉 Incredible job! You have completed all 12 milestones in your Career Roadmap!")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================== RENDER THE 4 PHASES ====================
    for phase in roadmap["phases"]:
        p_num = phase["phase_number"]
        p_title = phase["title"]
        p_dur = phase["duration"]
        p_desc = phase["description"]

        with st.expander(f"📍 {p_title} ({p_dur})", expanded=(p_num <= 2)):
            st.markdown(f"*{p_desc}*")
            st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

            if "tasks" in phase:
                for idx, t in enumerate(phase["tasks"]):
                    task_key = f"p1_task_{idx}"
                    is_checked = task_key in st.session_state["roadmap_completed_tasks"]
                    col_chk, col_txt = st.columns([0.08, 0.92])
                    with col_chk:
                        if st.checkbox("", value=is_checked, key=f"chk_{task_key}"):
                            st.session_state["roadmap_completed_tasks"].add(task_key)
                        else:
                            st.session_state["roadmap_completed_tasks"].discard(task_key)
                    with col_txt:
                        impact_color = "#F87171" if t.get("impact") in ["Critical", "High"] else "#60A5FA"
                        st.markdown(f"**{t['task']}**  \n<span style='font-size: 11.5px; color: {impact_color};'>Type: {t.get('type')} &nbsp;|&nbsp; Priority: {t.get('impact')}</span>", unsafe_allow_html=True)

            elif "skills_plan" in phase:
                for idx, sp in enumerate(phase["skills_plan"]):
                    st.markdown(f"#### 📘 {sp['skill']} — *{sp['duration']}*")
                    st.markdown(f"**Goal:** {sp['objective']}")
                    st.markdown("**Free Curated Learning Resources:**")
                    for r in sp["resources"]:
                        st.markdown(f"- 🔗 {r}")
                    
                    skill_key = f"p2_skill_{idx}"
                    is_checked = skill_key in st.session_state["roadmap_completed_tasks"]
                    if st.checkbox(f"Mastered core concepts and completed practice exercises for {sp['skill']}", value=is_checked, key=f"chk_{skill_key}"):
                        st.session_state["roadmap_completed_tasks"].add(skill_key)
                    else:
                        st.session_state["roadmap_completed_tasks"].discard(skill_key)
                    st.markdown("---")

            elif "projects" in phase:
                for idx, pr in enumerate(phase["projects"]):
                    st.markdown(f"#### 🛠️ {pr['project_title']}")
                    st.markdown("**Key Deliverables:**")
                    for d in pr["deliverables"]:
                        st.markdown(f"- {d}")
                    st.info(f"**Recommended Resume Bullet Point:**\n`{pr['recommended_bullet']}`")
                    
                    proj_key = f"p3_proj_{idx}"
                    is_checked = proj_key in st.session_state["roadmap_completed_tasks"]
                    if st.checkbox(f"Project built, tested, and pushed to GitHub: {pr['project_title']}", value=is_checked, key=f"chk_{proj_key}"):
                        st.session_state["roadmap_completed_tasks"].add(proj_key)
                    else:
                        st.session_state["roadmap_completed_tasks"].discard(proj_key)
                    st.markdown("---")

            elif "steps" in phase:
                for idx, step_item in enumerate(phase["steps"]):
                    step_key = f"p4_step_{idx}"
                    is_checked = step_key in st.session_state["roadmap_completed_tasks"]
                    col_chk, col_txt = st.columns([0.08, 0.92])
                    with col_chk:
                        if st.checkbox("", value=is_checked, key=f"chk_{step_key}"):
                            st.session_state["roadmap_completed_tasks"].add(step_key)
                        else:
                            st.session_state["roadmap_completed_tasks"].discard(step_key)
                    with col_txt:
                        st.markdown(f"**{step_item['step']}**  \n<span style='font-size: 11.5px; color: #34D399;'>Target: {step_item['timeline']}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("📝 Open Resume Maker to Implement Fixes", type="primary", use_container_width=True):
            st.session_state["current_page"] = "resume_maker"
            st.rerun()
    with col_act2:
        if st.button("🗺️ Explore Nearby Jobs Matching These Skills", use_container_width=True):
            st.session_state["current_page"] = "job_opportunities"
            st.rerun()
