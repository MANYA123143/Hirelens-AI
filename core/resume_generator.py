"""
HireLens AI - AI Resume Maker & Formatter
Provides blank canvas form data structures, AI bullet & summary enhancements,
and ATS-compliant HTML/Markdown/Text resume generation.
"""
import json

def generate_ai_summary(target_role: str, top_skills: str, experience_level: str = "Student/Fresher") -> str:
    """Generates an ATS-optimized professional summary based on user details."""
    skills_list = [s.strip() for s in top_skills.split(",") if s.strip()]
    skills_str = ", ".join(skills_list[:5]) if skills_list else "cutting-edge tools and methodologies"
    
    if "student" in experience_level.lower() or "fresher" in experience_level.lower():
        return (
            f"Ambitious and results-driven {target_role or 'Professional'} with strong foundation in {skills_str}. "
            f"Demonstrated ability to develop scalable solutions and collaborate across diverse academic and technical projects. "
            f"Eager to leverage analytical problem-solving and rapid learning capabilities to drive measurable impact in high-velocity teams."
        )
    else:
        return (
            f"Performance-oriented {target_role or 'Professional'} with hands-on expertise in {skills_str}. "
            f"Proven track record of optimizing workflows, architecting resilient systems, and driving cross-functional project success. "
            f"Dedicated to delivering measurable operational efficiencies and continuous technical innovation."
        )

def enhance_bullet_point(raw_bullet: str) -> str:
    """Enhances a raw bullet point with power action verbs and metrics."""
    bullet = raw_bullet.strip().lstrip("-*• ")
    if not bullet:
        return "Spearheaded core feature implementation, improving system throughput and enhancing team productivity by 25%."
    
    # Check if already starts with an action verb
    first_word = bullet.split()[0].lower()
    from config import ATS_ACTION_VERBS
    if first_word in ATS_ACTION_VERBS:
        # If it already has an action verb, check if it has a metric
        import re
        if not re.search(r'\d+%', bullet):
            return f"{bullet.rstrip('.')} — resulting in a 30% reduction in processing time."
        return bullet

    # Polish by prefixing with appropriate action verb
    return f"Spearheaded {bullet.lower().rstrip('.')} — boosting system performance and team efficiency by 25%."

def build_resume_text(data: dict) -> str:
    """Compiles the structured resume dictionary into clean plain text for ATS scoring."""
    lines = []
    
    # Personal Info
    p = data.get("personal", {})
    name = p.get("full_name", "Candidate Name").upper()
    title = p.get("title", "")
    lines.append(f"{name}")
    if title:
        lines.append(f"{title}")
    
    contact_parts = []
    if p.get("email"): contact_parts.append(p["email"])
    if p.get("phone"): contact_parts.append(p["phone"])
    loc = ", ".join(filter(None, [p.get("city"), p.get("state"), p.get("country")]))
    if loc: contact_parts.append(loc)
    if contact_parts:
        lines.append(" | ".join(contact_parts))

    links = []
    if p.get("linkedin"): links.append(f"LinkedIn: {p['linkedin']}")
    if p.get("github"): links.append(f"GitHub: {p['github']}")
    if p.get("portfolio"): links.append(f"Portfolio: {p['portfolio']}")
    if links:
        lines.append(" | ".join(links))
    lines.append("")

    # Summary
    if data.get("summary"):
        lines.append("PROFESSIONAL SUMMARY")
        lines.append(data["summary"].strip())
        lines.append("")

    # Skills
    skills = data.get("skills", {})
    if any(skills.values()):
        lines.append("SKILLS & COMPETENCIES")
        for cat, val in skills.items():
            if val:
                lines.append(f"• {cat}: {val}")
        lines.append("")

    # Experience
    exp_list = data.get("experience", [])
    if exp_list:
        lines.append("WORK EXPERIENCE")
        for exp in exp_list:
            role = exp.get("role", "")
            company = exp.get("company", "")
            loc = exp.get("location", "")
            dates = exp.get("dates", "")
            lines.append(f"{role} | {company} ({dates}) - {loc}")
            bullets = exp.get("bullets", "").split("\n")
            for b in bullets:
                if b.strip():
                    lines.append(f"  • {b.strip().lstrip('-*• ')}")
            lines.append("")

    # Education
    edu_list = data.get("education", [])
    if edu_list:
        lines.append("EDUCATION")
        for edu in edu_list:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            year = edu.get("year", "")
            gpa = edu.get("gpa", "")
            gpa_str = f" | GPA: {gpa}" if gpa else ""
            lines.append(f"{degree} - {institution} ({year}){gpa_str}")
            if edu.get("coursework"):
                lines.append(f"  Relevant Coursework: {edu['coursework']}")
        lines.append("")

    # Projects
    proj_list = data.get("projects", [])
    if proj_list:
        lines.append("KEY PROJECTS")
        for proj in proj_list:
            title = proj.get("title", "")
            tech = proj.get("tech_stack", "")
            desc = proj.get("description", "")
            tech_str = f" [{tech}]" if tech else ""
            lines.append(f"• {title}{tech_str}")
            if desc:
                for db in desc.split("\n"):
                    if db.strip():
                        lines.append(f"    - {db.strip().lstrip('-*• ')}")
        lines.append("")

    # Certifications
    if data.get("certifications"):
        lines.append("CERTIFICATIONS & HONORS")
        for c in data["certifications"].split("\n"):
            if c.strip():
                lines.append(f"• {c.strip().lstrip('-*• ')}")

    return "\n".join(lines)

def build_resume_html(data: dict) -> str:
    """Generates a professional ATS-compliant HTML/CSS resume template for live preview and printing."""
    p = data.get("personal", {})
    name = p.get("full_name", "Student Candidate")
    title = p.get("title", "Aspiring Professional")
    email = p.get("email", "")
    phone = p.get("phone", "")
    loc = ", ".join(filter(None, [p.get("city"), p.get("state"), p.get("country")]))
    linkedin = p.get("linkedin", "")
    github = p.get("github", "")
    portfolio = p.get("portfolio", "")

    summary = data.get("summary", "")
    skills = data.get("skills", {})
    experience = data.get("experience", [])
    education = data.get("education", [])
    projects = data.get("projects", [])
    certifications = data.get("certifications", "")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #1e293b;
            background: #ffffff;
            margin: 0;
            padding: 30px 40px;
            line-height: 1.45;
            font-size: 13.5px;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .name {{
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: 0.5px;
            margin: 0;
        }}
        .title {{
            font-size: 15px;
            font-weight: 600;
            color: #2563eb;
            margin: 4px 0 8px 0;
        }}
        .contact-info {{
            font-size: 12px;
            color: #475569;
        }}
        .contact-info span {{
            margin: 0 6px;
        }}
        .section-title {{
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 3px;
            margin-top: 14px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}
        .entry {{
            margin-bottom: 10px;
        }}
        .entry-header {{
            display: flex;
            justify-content: space-between;
            font-weight: 600;
            color: #0f172a;
        }}
        .entry-sub {{
            display: flex;
            justify-content: space-between;
            font-style: italic;
            color: #475569;
            font-size: 12.5px;
            margin-bottom: 4px;
        }}
        ul {{
            margin: 4px 0 0 18px;
            padding: 0;
        }}
        li {{
            margin-bottom: 3px;
            color: #334155;
        }}
        .skill-item {{
            margin-bottom: 4px;
        }}
        .skill-cat {{
            font-weight: 600;
            color: #1e293b;
        }}
        @media print {{
            body {{ padding: 15px 25px; }}
            .no-print {{ display: none; }}
        }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1 class="name">{name}</h1>
            <div class="title">{title}</div>
            <div class="contact-info">
                {f'<span>📧 {email}</span>' if email else ''}
                {f'<span>📱 {phone}</span>' if phone else ''}
                {f'<span>📍 {loc}</span>' if loc else ''}
                <br>
                {f'<span>🔗 <a href="{linkedin}" target="_blank">LinkedIn</a></span>' if linkedin else ''}
                {f'<span>💻 <a href="{github}" target="_blank">GitHub</a></span>' if github else ''}
                {f'<span>🌐 <a href="{portfolio}" target="_blank">Portfolio</a></span>' if portfolio else ''}
            </div>
        </div>
    """

    if summary:
        html += f"""
        <div class="section-title">Professional Summary</div>
        <p style="margin: 0; color: #334155;">{summary}</p>
        """

    if any(skills.values()):
        html += '<div class="section-title">Skills & Proficiencies</div>'
        for cat, val in skills.items():
            if val:
                html += f'<div class="skill-item"><span class="skill-cat">{cat}:</span> {val}</div>'

    if experience:
        html += '<div class="section-title">Work & Leadership Experience</div>'
        for exp in experience:
            role = exp.get("role", "")
            company = exp.get("company", "")
            eloc = exp.get("location", "")
            dates = exp.get("dates", "")
            bullets = [b.strip().lstrip("-*• ") for b in exp.get("bullets", "").split("\n") if b.strip()]
            
            html += f"""
            <div class="entry">
                <div class="entry-header">
                    <span>{role}</span>
                    <span>{dates}</span>
                </div>
                <div class="entry-sub">
                    <span>{company}</span>
                    <span>{eloc}</span>
                </div>
                <ul>
            """
            for b in bullets:
                html += f"<li>{b}</li>"
            html += "</ul></div>"

    if education:
        html += '<div class="section-title">Education</div>'
        for edu in education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            year = edu.get("year", "")
            gpa = edu.get("gpa", "")
            coursework = edu.get("coursework", "")
            
            html += f"""
            <div class="entry">
                <div class="entry-header">
                    <span>{institution}</span>
                    <span>{year}</span>
                </div>
                <div class="entry-sub">
                    <span>{degree}</span>
                    <span>{f"GPA: {gpa}" if gpa else ""}</span>
                </div>
                {f'<div style="font-size: 12px; color: #475569;">Coursework: {coursework}</div>' if coursework else ''}
            </div>
            """

    if projects:
        html += '<div class="section-title">Key Projects</div>'
        for proj in projects:
            p_title = proj.get("title", "")
            tech = proj.get("tech_stack", "")
            link = proj.get("link", "")
            desc_bullets = [b.strip().lstrip("-*• ") for b in proj.get("description", "").split("\n") if b.strip()]
            
            html += f"""
            <div class="entry">
                <div class="entry-header">
                    <span>{p_title} {f'<span style="font-size: 12px; color: #2563eb; font-weight: normal;">({tech})</span>' if tech else ''}</span>
                    {f'<span style="font-size: 12px;"><a href="{link}" target="_blank">View Code / Demo</a></span>' if link else ''}
                </div>
                <ul>
            """
            for b in desc_bullets:
                html += f"<li>{b}</li>"
            html += "</ul></div>"

    if certifications:
        html += '<div class="section-title">Certifications & Honors</div><ul>'
        for c in certifications.split("\n"):
            if c.strip():
                html += f"<li>{c.strip().lstrip('-*• ')}</li>"
        html += '</ul>'

    html += """
    </body>
    </html>
    """
    return html
