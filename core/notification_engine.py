"""
HireLens AI - Notification & Skills Matching Engine
Matches candidate skills and geographic location with live job openings and dispatches alerts.
"""
import re
from database.db import get_connection, create_notification, get_user_notifications

def calculate_skill_match(candidate_skills_str: str, job_skills_str: str) -> tuple[float, list[str]]:
    """Calculates percentage overlap between candidate skills and job required skills."""
    if not candidate_skills_str or not job_skills_str:
        return 0.0, []

    c_skills = {s.strip().lower() for s in re.split(r'[,|;/]', candidate_skills_str) if s.strip()}
    j_skills = {s.strip().lower() for s in re.split(r'[,|;/]', job_skills_str) if s.strip()}

    if not j_skills:
        return 0.0, []

    matched = []
    for js in j_skills:
        for cs in c_skills:
            if cs in js or js in cs:
                matched.append(js)
                break

    match_pct = round((len(matched) / len(j_skills)) * 100.0, 1)
    return match_pct, matched

def match_jobs_for_candidate(user: dict, min_match_pct: float = 40.0) -> list[dict]:
    """Finds matching jobs for a candidate based on skills and location."""
    user_skills = user.get("skills", "")
    user_city = (user.get("city") or "").lower().strip()
    user_state = (user.get("state") or "").lower().strip()
    user_category = user.get("target_category", "")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    all_jobs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    matches = []
    for job in all_jobs:
        job_skills = job.get("required_skills", "")
        pct, matched_skills = calculate_skill_match(user_skills, job_skills)
        
        # Location bonus
        loc_score = 0
        j_city = (job.get("city") or "").lower().strip()
        j_state = (job.get("state") or "").lower().strip()
        j_type = job.get("job_type", "")
        
        is_local = False
        if user_city and j_city == user_city:
            loc_score += 20
            is_local = True
        elif user_state and j_state == user_state:
            loc_score += 10
            is_local = True
        elif j_type == "Remote":
            loc_score += 15

        # Category match
        if user_category and job.get("category") == user_category:
            pct += 15

        total_score = min(100.0, pct + loc_score)
        if total_score >= min_match_pct or (is_local and len(matched_skills) >= 1):
            matches.append({
                "job": job,
                "total_score": round(total_score, 1),
                "skill_match_pct": pct,
                "matched_skills": matched_skills,
                "is_local": is_local
            })

    # Sort descending by match score
    matches.sort(key=lambda x: x["total_score"], reverse=True)
    return matches

def sync_user_job_notifications(user: dict):
    """Scans and inserts notifications for new matching jobs for this candidate."""
    if not user.get("notifications_enabled", 1):
        return 0

    user_id = user["id"]
    matches = match_jobs_for_candidate(user, min_match_pct=50.0)
    
    # Get existing notifications for this user
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT job_id FROM notifications WHERE user_id = ?", (user_id,))
    notified_job_ids = {r["job_id"] for r in cursor.fetchall() if r["job_id"] is not None}
    conn.close()

    count = 0
    for m in matches[:10]: # Limit to top 10 new matches
        job = m["job"]
        if job["id"] not in notified_job_ids:
            skills_str = ", ".join(m["matched_skills"][:3]) if m["matched_skills"] else "your target domain"
            loc_str = f" in {job['city']}, {job['state']}" if job['city'] else ""
            title = f"🔔 New Job Opportunity: {job['title']}"
            msg = (
                f"{job['company']} is hiring for '{job['title']}'{loc_str}! "
                f"Matches your skills: {skills_str}. Salary: {job['salary_range']}."
            )
            create_notification(
                user_id=user_id,
                job_id=job["id"],
                title=title,
                message=msg,
                matched_skills=", ".join(m["matched_skills"])
            )
            count += 1
    return count

def broadcast_job_to_candidates(job_id: int):
    """When a new job requirement is posted, alerts all matching registered candidates immediately."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        conn.close()
        return 0
    job = dict(job)

    cursor.execute("SELECT * FROM users WHERE notifications_enabled = 1")
    users = [dict(u) for u in cursor.fetchall()]
    conn.close()

    alerts_sent = 0
    for user in users:
        pct, matched = calculate_skill_match(user.get("skills", ""), job.get("required_skills", ""))
        user_city = (user.get("city") or "").lower()
        job_city = (job.get("city") or "").lower()
        same_city = user_city and (user_city == job_city)

        if pct >= 30.0 or same_city or user.get("target_category") == job.get("category"):
            matched_str = ", ".join(matched[:3]) if matched else "your profile"
            title = f"⚡ Instant Job Match: {job['title']} at {job['company']}"
            msg = (
                f"A new opening for {job['title']} in {job['city']}, {job['state']} matches your profile "
                f"({matched_str}) with a {pct}% skill fit!"
            )
            create_notification(
                user_id=user["id"],
                job_id=job["id"],
                title=title,
                message=msg,
                matched_skills=", ".join(matched)
            )
            alerts_sent += 1

    return alerts_sent
