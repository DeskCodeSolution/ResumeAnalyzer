import google.generativeai as genai
import pdf2image
import os
import io
import json
from dotenv import load_dotenv

load_dotenv()
import base64

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    # Combine all pages
    response = model.generate_content([input] + pdf_content + [prompt])

    return response.text

def get_gemini_response_keywords(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    # Combine all pages
    response = model.generate_content([input] + pdf_content + [prompt])
    return json.loads(response.text[8:-4])
    
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images (one per page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        pdf_parts = []
        for img in images:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            })

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")