import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path
import pytesseract
import pdfplumber

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Try direct text extraction
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"Direct text extraction failed: {e}")

    # Fallback to OCR for image-based PDFs
    print("Falling back to OCR for image-based PDF.")
    try:
        images = convert_from_path(pdf_path)
        for image in images:
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
    except Exception as e:
        print(f"OCR failed: {e}")

    return text.strip()

# Function to get response from Gemini AI
def generate_roadmap(resume_text, job_description=None):
    if not resume_text:
        return {"error": "Resume text is required for analysis."}
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    base_prompt = f"""
    You are an expert Career Development Coach specializing in {job_description} career paths. Your task is to create a detailed 12-week personalized roadmap for a student based on their resume analysis.

        RESUME ANALYSIS SUMMARY:

        Concisely list the relevant skills the applicant does not possess.
        Concisely Highlight Skills Relevant to the Job Description. 
        Suggest 5 specific projects (and a brief description of technologies) the candidate should make to learn the necessary skills and improve his pre-existing skills.
        Suggest specific courses (in the format Exact Course Name - Course Platform - Skills to Learn) that the candidate should take to improve his skills.

        - Current Skills: 
        - Skills to Develop: 
        - Suggested Projects: 
        - Suggested Courses: 
        - Career Goal: 

        ROADMAP REQUIREMENTS:
        1. Create a structured 12-week learning plan with specific weekly goals
        2. Each week must include:
        - Week number and theme/focus
        - 2-3 specific learning objectives
        - Recommended course modules or lessons (5-10 hours per week)
        - One hands-on mini-project or practical exercise 
        - Required resources and tools
        - Weekend review/assessment task

        3. Progressive difficulty curve:
        - Weeks 1-4: Foundational knowledge and basic skill building
        - Weeks 5-8: Intermediate concepts and applying skills to small projects
        - Weeks 9-12: Advanced topics and portfolio project development

        4. Incorporate the suggested courses and projects from the resume analysis
        5. Include specific milestones to track progress
        6. Estimate time commitment per day (aim for 2-3 hours on weekdays, 3-5 hours on weekends)
        7. Identify 3-5 measurable outcomes to achieve by the end of the roadmap

        FORMAT:
        - Present the roadmap as a structured, easy-to-follow plan
        - Use clear headings for each week
        - Use bullet points for activities and tasks
        - Include motivational elements and progress markers

        The roadmap should be personalized, realistic, and actionable - designed specifically for someone with the candidate's current skill level targeting a {job_description} position.
    
    Resume:
    {resume_text}
    """

    if job_description:
        base_prompt += f"""
        Additionally, compare this resume to the following job description:
        
        Job Description:
        {job_description}
        
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """

    response = model.generate_content(base_prompt)

    analysis = response.text.strip()
    return analysis


# Streamlit app


st.set_page_config(page_title="Roadmap Generator", page_icon="🗺️", layout="wide")
# Title
st.title("Personalized Roadmap Generator")
st.write("Analyze your resume and match it with your job goals, get a personalized roadmap made for you! . ")

col1 , col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
with col2:
    job_description = st.text_area("Enter Job Description:", placeholder="Paste the job description here...")

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")
else:
    st.warning("Please upload a resume in PDF format.")


st.markdown("<div style= 'padding-top: 10px;'></div>", unsafe_allow_html=True)
if uploaded_file:
    # Save uploaded file locally for processing
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Extract text from PDF
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume..."):
            try:
                # Analyze resume
                analysis = generate_roadmap(resume_text, job_description)
                st.success("Analysis complete!")
                st.write(analysis)
            except Exception as e:
                st.error(f"Analysis failed: {e}")

#Footer
st.markdown("---")
st.markdown("""<p style= 'text-align: center;' >Powered by <b>Streamlit</b> and <b>Google Gemini AI</b></p>""", unsafe_allow_html=True)