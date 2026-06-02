# 📄 ATS Resume Analyzer (AI Powered)

An AI-powered **ATS Resume Analyzer** built using Streamlit that evaluates how well a resume matches a job description using **NLP-based semantic similarity + skill extraction + ATS scoring logic**.

---
## Live demo
https://ats-resume-analyzer-dpfefuukdwsbdxoqt9uqin.streamlit.app/
---
## 🎯 Problem Statement

Recruiters spend only a few seconds scanning resumes. Many qualified candidates get rejected because their resumes are not optimized for Applicant Tracking Systems (ATS).  

This tool helps candidates understand:
- How well their resume matches a job description
- What skills are missing
- How to improve their chances of selection

---

## ✨ Features

- 📄 Upload resume in PDF format  
- 🧠 AI-powered semantic similarity scoring  
- 🎯 ATS score out of 100  
- 🔍 Skill extraction from resume & job description  
- ❌ Missing skills detection  
- 📊 Interactive visual dashboard (Plotly charts)  
- 📥 Downloadable report (TXT + CSV)  
- 💡 AI-generated recruiter-style feedback  
- 🎨 Modern animated UI (Streamlit styling)

---

## 🧠 Tech Stack

- Streamlit (Web App UI)
- Sentence Transformers (NLP embeddings)
- Scikit-learn (Cosine similarity)
- pdfplumber (PDF text extraction)
- Plotly (Data visualization)
- Pandas (Data handling)
- Regex (Skill extraction logic)

---

## 🏗️ Project Structure
ATS-Resume-Analyzer/
  ├── app.py           # Streamlit frontend + UI logic
  ├── utils.py         # NLP + scoring + skill extraction logic
  ├── requirements.txt # Project dependencies
  └── README.md

## ⚙️ How It Works

1. User uploads a resume (PDF)
2. Job description is pasted
3. Resume text is extracted using `pdfplumber`
4. Skills are detected using regex-based matching
5. Semantic similarity is calculated using SentenceTransformer embeddings
6. Final ATS score is computed:
   - Skill Match (weighted)
   - Semantic Similarity score
7. Missing skills are identified
8. Recruiter-style feedback is generated

---

## 📊 Scoring Logic

Final ATS Score =  
- 70% Skill Match  
- 30% Semantic Similarity  

This ensures both keyword matching and contextual understanding are considered.

---

## 📸 Screenshots


### ATS Dashboard
<img width="1240" height="1641" alt="ATS Resume Analyzer · Streamlit_page-0001" src="https://github.com/user-attachments/assets/ce2a2f96-b4db-4e69-ad62-3d092896bd7b" />


### Skill Analysis View

<img width="1240" height="1657" alt="ATS Resume Analyzer · Streamlit_page-0002" src="https://github.com/user-attachments/assets/b69cf47d-cde0-4e4c-8862-c9b00c62f13a" />

---

## 📌 Example Output

- ATS Score: **82 / 100**
- Resume Skills: python, sql, machine learning, pandas  
- Job Skills: python, sql, machine learning, docker, aws  
- Missing Skills: docker, aws  
- Feedback: Strong ATS match with minor skill gaps

---

## 🚀 Key Highlights

- Combines **traditional ATS keyword matching + modern NLP embeddings**
- Lightweight and fast Streamlit web app
- Real-world HR/recruitment use case
- Beginner-friendly AI project with strong portfolio value

---

## 🔮 Future Improvements

- Multi-resume ranking system  
- AI-powered resume rewriting suggestions  
- Job recommendation engine  
- User authentication system  
- PDF report generator with branding  
- Database storage for resume history  

---

## 👨‍💻 Author

Built as an AI portfolio project demonstrating NLP, semantic search, and real-world ATS simulation.

---

## 📜 License

This project is open for educational and portfolio use.
