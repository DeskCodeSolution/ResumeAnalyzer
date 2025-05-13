# Resume Analyzer

A Streamlit web application that analyzes resumes against job descriptions using Google Gemini AI. The app provides ATS-style feedback, keyword extraction, percentage match, and resume parsing.

## Features

- **Resume Analysis:** Get professional feedback on how well a resume matches a job description.
- **Keyword Extraction:** Identify technical, analytical, and soft skills required for the job.
- **Percentage Match:** See how closely a resume matches the job description, including missing keywords.
- **Resume Parsing:** Extract key details (name, contact, skills, profiles, etc.) from the resume.

## How It Works

1. **Upload your resume** in PDF format.
2. **Paste the job description** into the provided text area.
3. **Choose an action** by clicking one of the following buttons:
   - Tell Me About the Resume
   - Get Keywords
   - Percentage Match
   - Parse Resume

The app uses Google Gemini AI to process the resume and job description, returning results directly in the browser.

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd ResumeAnalyzer
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Create a `.env` file in the project root directory and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_google_gemini_api_key
     ```

4. **Run the app:**
   ```sh
   streamlit run main.py
   ```

## File Structure

- `main.py` - Streamlit app UI and logic
- `helper_func.py` - Helper functions for PDF processing and Gemini API calls
- `requirements.txt` - Python dependencies
- `.env` - API key (not tracked in git)
- `.gitignore` - Files and folders to ignore in git

## Requirements

- Python 3.10+
- Google Gemini API access

## License

This project is for educational/demo purposes only.