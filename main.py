import streamlit as st
from helper_func import input_pdf_setup, get_gemini_response, get_gemini_response_keywords
import json

## Streamlit App

st.set_page_config(page_title="ATS Resume Scanner")
st.title("ATS Tracking System")
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

input_prompt4 = """
You are a professional-grade resume parser. Analyze the resume text provided below and extract the following details accurately
there can be multiple work experiences so analyze whole text very carefully and return an array as output in the following format:
if some of information is not present in the resume then return null in the output. do not make up the answer only answer from resume provided.
and extract username of github and linkdin carefully it should be always accurate.
if grade are in CGPA then mention CGPA in the grade field.

Return the output in the following JSON format:
{
  "name": "<Full Name>",
  "github": "<GitHub Profile or Username>",
  "linkedin": "<LinkedIn Profile or Username>",
  "email": "<Email Address>",
  "contact": "<Contact Number>",

  "total work experience":[
    {
      "company name": "<Company Name>",
      "job title": "<Job Title>",
      "start date": "<Start Date>",
      "end date": "<End Date>"
    },
    {
      "company name": "<Company Name>",
      "job title": "<Job Title>",
      "start date": "<Start Date>",
      "end date": "<End Date>",
    }
  ],
  "education":[
    {
      "qualification": "<Qualification >",
      "institution": "<institute Or School Name",
      "start_year": <Start Date>,
      "end_year": <End Time>,
      "grade": <grade in percentage or CGPA>
    },
    {
      "qualification": "<Qualification >",
      "institution": "<institute Or School Name",
      "start_year": <Start Date>,
      "end_year": <End Time>,
      "grade": <grade in percentage or CGPA>
    },

  ]
  "hobbies":[
    "<Hobby 1>",
    "<Hobby 2>",
    "<Hobby 3>"
  ],
  "address": "<Address>",
  "skills": ["<Skill 1>", "<Skill 2>", "..."]
}

if in the end date is present then write present in the end date
and the make json format proper so that it can be parsed easily.

"""

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
        st.header("The Repsonse is")
        
        response = response[7:]
        tick = response[-1]
        while(tick != '}'):
            response = response[:-1]
            tick = response[-1]
        
        response = json.loads(response)
        filename = ""
        for i in response['name']:
            if i !=" ":
                filename+= i
            else:
                filename +="_"
        with open(f"{filename}.json", "w") as outfile:
            json.dump(response, outfile, indent=4)
        
        st.write(f"Full Name: {response['name']}")
        if response['github'] != None:
            st.write(f"GitHub Profile URL or Username: {response['github']}")
        if response['linkedin'] != None or response['linkedin'] != "None"   :
            st.write(f"LinkedIn Profile URL or Username: {response['linkedin']}")
        if response['email'] != None or response['email'] != "None":
            st.write(f"Email Address: {response['email']}")
        if response['contact'] != None or response['contact'] != "None":
            st.write(f"Contact Number: {response['contact']}")
        if response['address'] != None or response['address'] != "None":
            st.write(f"Address: {response['address']}") 
        if response['education'] != None or response['education'] != "None":
            st.subheader("Education:")
            for i in range(len(response['education'])):
                st.write(f"Qualification: {response['education'][i]['qualification']}")
                st.write(f"Institution: {response['education'][i]['institution']}")
                st.write(f"Start Year: {response['education'][i]['start_year']}")
                st.write(f"End Year: {response['education'][i]['end_year']}")
                st.write(f"Grade: {response['education'][i]['grade']}")
        if response['total work experience'] != None or response['total work experience'] != "None":
            st.subheader("Work Experience:")
            for i in range(len(response['total work experience'])):

                st.write(f"Company Name: {response['total work experience'][i]['company name']}")
                st.write(f"Job Title: {response['total work experience'][i]['job title']}")
                st.write(f"Start Date: {response['total work experience'][i]['start date']}")
                st.write(f"End Date: {response['total work experience'][i]['end date']}")
        if response['skills'] != None or response['skills'] != "None":
            st.subheader("Skills:")
            for skill in response['skills']:
                st.markdown(f"- {skill}")

        if response['hobbies'] :
            st.subheader("Hobbies:")
            for i in range(len(response['hobbies'])):
                st.markdown(f"Hobby: {response['hobbies'][i]}")
    else:
        st.write("Please upload the resume")