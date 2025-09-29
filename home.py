import streamlit as st

st.set_page_config(
    page_title="Resume Analyzer Hub",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Resume Analyzer Hub")
st.markdown("""
### Welcome to your all-in-one Resume Analysis Platform!

This platform provides three powerful tools:

1. **👔 Student Resume Analyzer** - For students to analyze their resumes and get improvement suggestions
2. **🤝 Interviewer Resume Analyzer** - For recruiters to evaluate candidate resumes  
3. **🗺️ Roadmap Generator** - Generate a personalized 12-week learning roadmap

**Use the sidebar to navigate between tools!**
""")

st.info("👈 Select a tool from the sidebar to get started!")