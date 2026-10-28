import streamlit as st
import pandas as pd
from datetime import datetime
import PyPDF2
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Job Skill Analyzer", layout="wide")
st.title("Smart Job Skill Analyzer")

# ---------- SESSION STATE ----------
if 'analyze_clicked' not in st.session_state:
    st.session_state['analyze_clicked'] = False

# ---------- INPUTS ----------
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Name *")
    job_role = st.text_input("Target Job Role *")
with col2:
    company = st.text_input("Company Name *")
    location = st.text_input("Job Location *")
with col3:
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

mandatory_filled = all([name, job_role, company, location, uploaded_file])

# ---------- ANALYZE BUTTON ----------
if mandatory_filled:
    if st.button("Analyze"):
        st.session_state['analyze_clicked'] = True

# ---------- JOB SKILLS DATABASE ----------
all_job_skills = {
    "data analyst": ["Python", "SQL", "Excel", "Power BI", "Statistics", "Communication"],
    "business analyst": ["Excel", "SQL", "PowerPoint", "Requirement Gathering", "Stakeholder Management"],
    "software developer": ["Python", "Java", "SQL", "Git", "Problem Solving"],
    "teacher": ["Subject Knowledge", "Communication", "Lesson Planning", "Patience", "Time Management"],
    "nurse": ["Patient Care", "Medical Knowledge", "Empathy", "Communication", "Attention to Detail"],
    "chef": ["Cooking Skills", "Time Management", "Creativity", "Hygiene", "Teamwork"],
    "sales executive": ["Communication", "Negotiation", "CRM", "Persuasion", "Networking"]
}

# ---------- COMPANY HIRING DATA ----------
company_hiring = pd.DataFrame({
    "Company": ["TCS", "Infosys", "Wipro", "Accenture", "Schools", "Hospitals", "Restaurants"],
    "Location": ["Chennai", "Bangalore", "Hyderabad", "Pune", "Delhi", "Mumbai", "Bangalore"],
    "Role": ["Data Analyst", "Business Analyst", "Data Analyst", "Software Developer", "Teacher", "Nurse", "Chef"],
    "Required Skills": [
        "Python, SQL, Power BI",
        "Excel, PPT, Requirement Gathering",
        "Python, SQL, Excel",
        "Python, Java, Git",
        "Subject Knowledge, Communication, Lesson Planning",
        "Patient Care, Medical Knowledge, Empathy",
        "Cooking Skills, Time Management, Creativity"
    ]
})

# ---------- ANALYSIS ----------
matched, missing = [], []
target_skills = []
salary_range = ""

if st.session_state['analyze_clicked'] and uploaded_file:
    # Extract text from PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text().lower()

    resume_skills = resume_text.split()
    target_skills = all_job_skills.get(job_role.lower(), [])

    matched = list(set(resume_skills) & set([s.lower() for s in target_skills]))
    missing = list(set([s.lower() for s in target_skills]) - set(resume_skills))

    # ---------- Matched & Missing Skills ----------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='color:green'>Matched Skills</h3>", unsafe_allow_html=True)
        for m in matched:
            st.markdown(f"• {m.upper()}")
    with col2:
        st.markdown("<h3 style='color:red'>Missing Skills</h3>", unsafe_allow_html=True)
        for m in missing:
            st.markdown(f"• {m.upper()}")

    # ---------- Career Recommendation with Star Points ----------
    st.markdown("<h4 style='color:purple'>Career Recommendation</h4>", unsafe_allow_html=True)

    strengths = ', '.join([m.upper() for m in matched]) if matched else "None yet"
    top_missing = missing[:3] if missing else []
    opportunities = ', '.join([s.title() for s in top_missing]) if top_missing else "None"

    if len(matched)/len(target_skills) >= 0.8:
        next_steps = f"Apply confidently for {job_role.title()} roles or take advanced courses to grow further."
    elif len(matched)/len(target_skills) >= 0.5:
        next_steps = f"Focus on improving missing skills to strengthen your profile: {opportunities}."
    else:
        next_steps = f"Explore entry-level or related roles while building skills: {opportunities}."

    st.markdown(f"""
★ Strengths: {strengths}  
★ Opportunities: {opportunities}  
★ Next Steps: {next_steps}
""")

    # ---------- Salary Packages ----------
    salary_map = {
        "data analyst": "₹6L – ₹10L",
        "business analyst": "₹5L – ₹9L",
        "software developer": "₹7L – ₹12L",
        "teacher": "₹3L – ₹6L",
        "nurse": "₹3.5L – ₹7L",
        "chef": "₹2.5L – ₹5L",
        "sales executive": "₹4L – ₹8L"
    }
    salary_range = salary_map.get(job_role.lower(), "Not Available")
    st.markdown(f"**Estimated Salary Range for {job_role.title()}: {salary_range} per year**")

    # ---------- Company Match Table ----------
    st.markdown("<h3 style='color:#333333'>Company Match Overview</h3>", unsafe_allow_html=True)
    filtered = company_hiring[company_hiring["Role"].str.lower() == job_role.lower()]
    st.markdown(filtered.to_html(index=False), unsafe_allow_html=True)

    # ---------- Top Future Demand Skills Graph ----------
    st.markdown("<h3 style='color:#333333'>Top Future Demand Skills</h3>", unsafe_allow_html=True)
    demand_scores_default = {skill: 80 + i*3 for i, skill in enumerate(target_skills)}
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(demand_scores_default.keys(), demand_scores_default.values(), color='#28a745')
    ax.set_ylabel('Demand Score')
    ax.set_xlabel('Skills')
    ax.set_ylim(0, 100)
    ax.set_title(f'{job_role.title()} - Skill Demand')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # ---------- Skill Insights Summary (END OF PAGE) ----------
    skill_gap_pct = round(len(missing)/len(target_skills)*100) if target_skills else 0
    st.subheader("Skill Insights Summary")
    st.markdown(f"""
**Total Required Skills:** {len(target_skills)}  
**Matched Skills:** {len(matched)} → {', '.join([m.upper() for m in matched]) if matched else 'None'}  
**Missing Skills:** {len(missing)} → {', '.join([s.title() for s in missing]) if missing else 'None'}  
**Estimated Skill Gap:** {skill_gap_pct}%
""")

# ---------- SAVE RESULTS BUTTON ----------
if st.button("Save Results"):
    if matched or missing:
        df = pd.DataFrame([{
            "Name": name,
            "Job Role": job_role,
            "Company": company,
            "Location": location,
            "Matched Skills": matched,
            "Missing Skills": missing,
            "Salary Range": salary_range,
            "Time": str(datetime.now())
        }])
        df.to_csv("saved_analysis.csv", index=False)
        st.markdown('<p style="color:#28a745; font-weight:bold;">Saved Successfully ✅</p>', unsafe_allow_html=True)