from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
import fitz
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)  # Fixed method call
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes()

        pdf_parts = [
            {"mime_type": "image/jpeg",
             "data": base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI setup
st.set_page_config(page_title="My Intelligent ATS Resume Expert")
st.header("My Intelligent ATS Expert")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully...")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage Match")

input_prompt_1 = """
You are an experienced student in the tech department, evaluating resumes for roles in data science,
full-stack development, web development, big data engineering, and data analysis.
Review the provided resume against the job description and share your evaluation, highlighting the strengths
and weaknesses of the candidate in relation to the specified job roles.
"""

input_prompt_2 = """
You are an experienced student in the tech department, evaluating resumes for roles in data science,
full-stack development, web development, big data engineering, and data analysis.
Evaluate the resume against the provided job description and provide the percentage match,
missing keywords, and final comments.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_1)
        st.subheader("The Response Is:")
        st.write(response)
    else:
        st.write("Please upload the resume.")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_2)
        st.subheader("The Response Is:")
        st.write(response)
    else:
        st.write("Please upload the resume.")
