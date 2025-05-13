import streamlit as st
from helper_func import input_pdf_setup, get_gemini_response, get_gemini_response_keywords
import json

## Streamlit App

st.set_page_config(page_title="ATS Resume Scanner")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

col1, col2, col3 , col4  = st.columns(4,gap="medium")

with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Get Keywords")

with col3:
    submit3 = st.button("Percentage match")

with col4:
    submit4 = st.button("Parse Resume")



input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
As an expert ATS (Applicant Tracking System) scanner with an in-depth understanding of AI and ATS functionality, 
your task is to evaluate a resume against a provided job description. Please identify the specific skills and keywords 
necessary to maximize the impact of the resume and provide responde in json format as {Technical Skills:[], Analytical Skills:[], Soft Skills:[]}.
Note: Please do not make up the answer only answer from job description provided"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts. 
"""

input_prompt4 =""" You are an advanced resume parser. Analyze the resume text provided below and extract the following details accurately:

Full Name

GitHub Profile URL or Username

LinkedIn Profile URL or Username

Email Address

Contact Number

Total Work Experience (in years/months or date range)

Address (full address or city/state if detailed address is unavailable)

Skills (list of technical, professional, or soft skills)

Return the output strictly in the following JSON format: """

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response_keywords(input_prompt2,pdf_content,input_text)

        st.subheader("Skills are:")
        if response != None:
            st.write(f"Technical Skills: {', '.join(response['Technical Skills'])}.")
            st.write(f"Analytical Skills: {', '.join(response['Analytical Skills'])}.")
            st.write(f"Soft Skills: {', '.join(response['Soft Skills'])}.")
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Repsonse is")
        
        response = response[7:]
        tick = response[-1]
        while(tick != '}'):
            response = response[:-1]
            tick = response[-1]
        response = json.loads(response)
        
        
        st.write(f"Full Name: {response['Full Name']}")
        if response['GitHub Profile URL or Username'] != None:
            st.write(f"GitHub Profile URL or Username: {response['GitHub Profile URL or Username']}")
        if response['LinkedIn Profile URL or Username'] != None:
            st.write(f"LinkedIn Profile URL or Username: {response['LinkedIn Profile URL or Username']}")
        if response['Email Address'] != None:
            st.write(f"Email Address: {response['Email Address']}")
        if response['Contact Number'] != None:
            st.write(f"Contact Number: {response['Contact Number']}")
        if response['Total Work Experience (in years/months or date range)'] != None:
            st.write(f"Total Work Experience: {response['Total Work Experience (in years/months or date range)']}")
        if response['Address (full address or city/state if detailed address is unavailable)'] != None:
            st.write(f"Address: {response['Address (full address or city/state if detailed address is unavailable)']}")
        if response.get('Skills') and isinstance(response['Skills'], list):
            st.write("Skills:")
            for skill in response['Skills']:
                st.markdown(f"- {skill}")
    else:
        st.write("Please upload the resume")