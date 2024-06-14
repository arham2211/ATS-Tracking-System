import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf):
    combined_text = input + "\n" + pdf
    model =  genai.GenerativeModel("gemini-pro")
    response = model.generate_content(combined_text)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    print(text)
    return text


#Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key = "input")


uploaded_file = st.file_uploader("Upload Your Resume...", type="pdf")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How can i Improvise my skills")
submit3 = st.button("Percentage Match")


input_prompt1 = """

You are an expert in evaluating resumes,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

"""
input_prompt2 = """

You are an expert in skill enhancement. Users seek your guidance on how to improvise their existing skills 
and excel in their fields. They are looking for practical suggestions on refining 
their abilities, such as practicing advanced techniques, seeking mentorship, or exploring new 
approaches. Your role is to provide tailored recommendations to help users enhance their skills and stay 
competitive in their respective industries. Your insights will empower users to progress in their careers and achieve their professional aspirations.


"""

input_prompt3 = """


You are an expert in job application strategies. Users will provide details about their qualifications and the job they are applying for. 
Your task is to assess the match between the user's profile and the job requirements. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.

"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
