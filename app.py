import streamlit as st
import docx2txt
from pdfminer.high_level import extract_text as extract_pdf_text
from analyzer import get_feedback_from_model
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# ---- UI CONFIG ----
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🧠 AI-Powered Resume Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown("Upload your **resume** and paste a **job description** to get smart AI-generated feedback on how well your resume matches the role — and what to improve.")
st.markdown("---")

# ---- INPUT SECTION ----
col1, col2 = st.columns([1, 2])

with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    job_text = st.text_area("📝 Paste Job Description", height=200)

# ---- ANALYZE BUTTON ----
if st.button("🚀 Analyze Resume", use_container_width=True):
    if not resume_file or not job_text:
        st.warning("⚠️ Please upload a resume and paste the job description.")
    else:
        # ---- RESUME TEXT EXTRACTION ----
        try:
            if resume_file.name.endswith(".pdf"):
                resume_text = extract_pdf_text(resume_file)
            else:
                resume_text = docx2txt.process(resume_file)
        except Exception as e:
            st.error(f"❌ Failed to extract text from resume. Error: {e}")
            st.stop()

        # ---- DISPLAY RESUME PREVIEW ----
        with st.expander("📖 Resume Preview"):
            st.text_area("Extracted Resume Text", resume_text, height=250)

        with st.expander("📋 Job Description Preview"):
            st.text_area("Job Description Text", job_text, height=250)

        # ---- AI FEEDBACK ----
        with st.spinner("🧠 Analyzing resume with Google Gemini... please wait..."):
            try:
                feedback = get_feedback_from_model(resume_text, job_text)
            except Exception as e:
                st.error(f"❌ Gemini API Error: {e}")
                st.stop()

        st.markdown("---")
        st.markdown("### 📋 AI Feedback Report")
        st.markdown(
            f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 8px; border-left: 5px solid #4B8BBE;'>"
            f"<pre style='white-space: pre-wrap;'>{feedback}</pre>"
            f"</div>",
            unsafe_allow_html=True
        )
