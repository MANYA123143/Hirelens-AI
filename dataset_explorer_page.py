"""
HireLens AI - Hugging Face Kaggle-Resume Dataset Explorer
Interactive visualization, skill taxonomies, and search across 2,484 resumes from Divyaamith/Kaggle-Resume.
"""
import streamlit as st
import plotly.graph_objects as go
try:
    from core.dataset_loader import DatasetEngine
except ModuleNotFoundError:
    from dataset_loader import DatasetEngine
from config import KAGGLE_CATEGORIES

def render_dataset_explorer():
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #1e3a8a; margin-bottom: 4px;">
            📊 Hugging Face Kaggle-Resume Dataset Intelligence
        </h2>
        <p style="color: #64748b; margin: 0;">
            Direct integration with <code>Divyaamith/Kaggle-Resume</code> (2,484 resumes, 24 distinct domain categories).
        </p>
    </div>
    """, unsafe_allow_html=True)

    engine = DatasetEngine.get_instance()
    counts = engine.get_category_counts()

    # Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Resumes in Dataset", f"{sum(counts.values()):,}")
    with c2:
        st.metric("Domain Categories", f"{len(counts)}")
    with c3:
        st.metric("Dataset Source", "Hugging Face")
    with c4:
        st.metric("Primary Format", "CSV / Text / HTML")

    st.markdown("<br>", unsafe_allow_html=True)

    tab_overview, tab_browser, tab_taxonomies = st.tabs([
        "📈 Category Distribution & Analytics",
        "🔍 Resume Explorer & Search",
        "🧠 Benchmark Skill Taxonomies"
    ])

    # ==================== OVERVIEW & CHARTS ====================
    with tab_overview:
        st.subheader("Category Distribution (24 Domains)")
        
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        categories = [item[0] for item in sorted_counts]
        resume_numbers = [item[1] for item in sorted_counts]

        fig = go.Figure(go.Bar(
            x=categories,
            y=resume_numbers,
            marker_color='#2563eb',
            hoverinfo='x+y'
        ))
        fig.update_layout(
            title="Number of Resumes per Domain in Divyaamith/Kaggle-Resume",
            xaxis_title="Domain / Category",
            yaxis_title="Count of Resumes",
            xaxis_tickangle=-45,
            height=450,
            margin=dict(l=20, r=20, t=40, b=100)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption("ℹ️ Dataset Citation: Divyaamith/Kaggle-Resume on Hugging Face Hub (scraped from live career archives for NLP & resume classification).")

    # ==================== BROWSE RESUMES ====================
    with tab_browser:
        st.subheader("Search & Inspect Benchmark Resumes")
        
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            sel_cat = st.selectbox("Filter by Category", ["All"] + KAGGLE_CATEGORIES, index=0, key="explorer_cat_filter")
        with col_s2:
            search_term = st.text_input("Search Keyword within Resumes", placeholder="e.g. machine learning, audit, salesforce", key="explorer_search")

        results = engine.search_resumes(keyword=search_term, category=sel_cat, limit=12)
        st.write(f"Found **{len(results)} sample resumes**:")

        for r in results:
            with st.expander(f"📄 Resume ID: {r['id']} | Category: {r['category']}"):
                st.markdown(f"**Domain:** `{r['category']}`")
                st.markdown("**Preview Snippet:**")
                st.text(r["snippet"] + "...")
                
                col_b1, col_b2 = st.columns([1, 3])
                with col_b1:
                    if st.button("⚡ Test in ATS Checker", key=f"test_ats_{r['id']}"):
                        st.session_state["resume_to_analyze"] = r["full_text"]
                        st.session_state["current_page"] = "ats_analyzer"
                        st.rerun()
                with col_b2:
                    st.download_button(
                        label="📥 Download Full Resume Text",
                        data=r["full_text"],
                        file_name=f"Kaggle_Resume_{r['id']}.txt",
                        mime="text/plain",
                        key=f"dl_{r['id']}"
                    )

    # ==================== SKILL TAXONOMIES ====================
    with tab_taxonomies:
        st.subheader("Extracted Benchmark Skills per Domain")
        st.write("These skill taxonomies are utilized by the HireLens ATS Scorer and Notification Engine to identify candidate gaps and match opportunities.")

        tax_cols = st.columns(2)
        for idx, (cat, skills) in enumerate(engine.category_skills.items()):
            col = tax_cols[idx % 2]
            with col:
                with st.container(border=True):
                    st.markdown(f"#### 🏷️ {cat}")
                    skills_tags = "".join([f'<span class="skill-badge">{s}</span>' for s in skills])
                    st.markdown(skills_tags, unsafe_allow_html=True)
