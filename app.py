import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    extract_text_from_pdf,
    calculate_ats_score,
    missing_skills,
    recruiter_feedback
)

# ---------------- MODEL CACHE (IMPORTANT FIX) ----------------
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Make model available to utils if needed
import utils
utils.model = model

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ATS Resume Analyzer",
    layout="wide"
)

# ---------------- UI STYLING ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #ffecd2, #fcb69f, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.block-container {
    background: transparent !important;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #111827;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.85);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    border-left: 5px solid #6366f1;
}

.stDownloadButton button {
    background: linear-gradient(90deg,#6366f1,#ec4899,#06b6d4);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
}

textarea {
    background: rgba(255,255,255,0.9) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("# 📄 ATS Resume Analyzer")
st.markdown("AI-powered resume screening using NLP + ATS scoring system")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_desc = st.text_area("Paste Job Description", height=300)

# ---------------- HIGH PRIORITY SKILLS ----------------
HIGH_PRIORITY_SKILLS = {"python", "sql", "machine learning", "deep learning", "nlp"}

# ---------------- MAIN LOGIC ----------------
if resume_file and job_desc:

    # Reset file pointer (safe fix)
    resume_file.seek(0)

    # Extract text
    resume_text = extract_text_from_pdf(resume_file)

    # ATS scoring
    score, resume_skills, job_skills = calculate_ats_score(resume_text, job_desc)

    score_display = round(score, 2)
    score_int = int(round(score))

    # Missing skills
    missing = missing_skills(resume_text, job_desc)
    feedback = recruiter_feedback(score_display, missing)

    # ---------------- DASHBOARD ----------------
    st.markdown("## 📊 ATS Analysis Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Score", f"{score_display}/100")
    c2.metric("Resume Skills", len(resume_skills))
    c3.metric("Job Skills", len(job_skills))

    st.progress(score_int)

    # Status message
    if score_display >= 80:
        st.success("Strong ATS Match")
    elif score_display >= 50:
        st.warning("Moderate ATS Match")
    else:
        st.error("Weak ATS Match")

    st.markdown("---")

    # ---------------- PIE CHART ----------------
    fig = go.Figure(data=[go.Pie(
        labels=["Match", "Gap"],
        values=[score_int, 100 - score_int],
        hole=0.55,
        marker_colors=["#6366f1", "#ec4899"]
    )])

    fig.update_layout(title="ATS Match Breakdown")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- SKILLS ----------------
    st.markdown("### 🧠 Resume Skills")
    st.write(resume_skills if resume_skills else "No skills detected")

    st.markdown("### 📌 Job Skills")
    st.write(job_skills if job_skills else "No job skills detected")

    st.markdown("### ❌ Missing Skills")
    st.write(missing if missing else "No missing skills")

    # ---------------- BAR CHART ----------------
    if missing:
        colors = [
            "#ff0000" if skill in HIGH_PRIORITY_SKILLS else "#ec4899"
            for skill in missing
        ]

        bar_fig = go.Figure(go.Bar(
            x=[1] * len(missing),
            y=missing,
            orientation='h',
            marker=dict(color=colors),
            text=missing,
            textposition='inside'
        ))

        bar_fig.update_layout(
            title="Missing Skills (Red = High Priority)",
            xaxis=dict(visible=False),
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(bar_fig, use_container_width=True)

    # ---------------- FEEDBACK ----------------
    st.markdown("### 💡 Recruiter AI Feedback")
    st.info(feedback)

    # ---------------- DOWNLOAD REPORT ----------------
    report_txt = f"""
ATS RESUME ANALYSIS REPORT

ATS Score: {score_display}/100

Resume Skills: {resume_skills}
Job Skills: {job_skills}
Missing Skills: {missing}
Feedback: {feedback}
"""

    st.download_button(
        "Download TXT Report",
        report_txt,
        file_name="ATS_Report.txt"
    )

    # CSV report
    max_len = max(len(resume_skills), len(job_skills), len(missing))

    resume_pad = resume_skills + [""] * (max_len - len(resume_skills))
    job_pad = job_skills + [""] * (max_len - len(job_skills))
    missing_pad = missing + [""] * (max_len - len(missing))

    df = pd.DataFrame({
        "Resume Skills": resume_pad,
        "Job Skills": job_pad,
        "Missing Skills": missing_pad
    })

    st.download_button(
        "Download CSV Report",
        df.to_csv(index=False),
        file_name="ATS_Report.csv"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.write(" ATS Resume Analyzer • AI + NLP Portfolio Project")