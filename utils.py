import pdfplumber
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- MODEL (INJECTED FROM app.py) ----------------
model = None

# ---------------- KNOWN SKILLS DATABASE ----------------
KNOWN_SKILLS = {
    # Programming
    "python", "java", "sql", "r", "c++",

    # AI / ML
    "machine learning", "deep learning", "data science",
    "data analysis", "statistics", "nlp",
    "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch",

    # Visualization
    "tableau", "power bi", "excel",
    "dashboard", "visualization",

    # Data Engineering
    "etl", "elt", "spark", "hadoop",
    "data warehouse", "data engineering",

    # Cloud / DevOps
    "aws", "azure", "gcp",
    "docker", "kubernetes",

    # Business / Analytics
    "fraud", "claims", "underwriting",
    "risk", "compliance",
    "forecasting", "reporting",
    "business intelligence"
}

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(file):
    """
    Extract text from PDF using pdfplumber
    """
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

    except Exception as e:
        raise RuntimeError(f"PDF reading error: {e}")

    return text.lower()


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    """
    Extract known skills using regex matching
    """
    text = text.lower()
    found_skills = set()

    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(list(found_skills))


# ---------------- SEMANTIC SIMILARITY ----------------
def semantic_score(resume_text, job_desc):
    """
    Compute cosine similarity using SentenceTransformer embeddings
    """
    if model is None:
        raise ValueError("Model not loaded. Ensure app.py injects the model.")

    embeddings = model.encode([resume_text, job_desc])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score * 100)


# ---------------- ATS SCORE ----------------
def calculate_ats_score(resume_text, job_desc, skill_weight=0.7):
    """
    Final ATS score = skill match + semantic similarity
    """

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_desc))

    # Skill match ratio
    if len(job_skills) == 0:
        skill_score = 0
    else:
        skill_score = len(resume_skills & job_skills) / len(job_skills)

    # Semantic similarity
    semantic = semantic_score(resume_text, job_desc) / 100

    # Final weighted score
    final_score = (skill_weight * skill_score + (1 - skill_weight) * semantic) * 100

    return round(final_score, 2), sorted(list(resume_skills)), sorted(list(job_skills))


# ---------------- MISSING SKILLS ----------------
def missing_skills(resume_text, job_desc):
    """
    Return skills required in job but missing in resume
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_desc))

    return sorted(list(job_skills - resume_skills))


# ---------------- RECRUITER FEEDBACK ----------------
def recruiter_feedback(score, missing):
    """
    Human-like ATS feedback generator
    """

    if score >= 80:
        status = "Strong ATS Match"
    elif score >= 50:
        status = "Moderate ATS Match"
    else:
        status = "Weak ATS Match"

    if missing:
        return f"{status}. Missing key skills: {', '.join(missing[:6])}"
    else:
        return f"{status}. No major skill gaps detected."