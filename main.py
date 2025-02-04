from fastapi import FastAPI, File, UploadFile
import shutil
import fitz  # PyMuPDF for PDF text extraction
from docx import Document  # python-docx for DOCX files
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# crete a folder to store uploaded resume

UPLOAD_FOLDER="uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTMLResponse(open("static/index.html").read())

# API to upload resumes

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text based on file type
    if file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type"}

    # Analyze resume text
    analysis = analyze_resume(extracted_text)

    # Generate AI Roast
    roast = generate_roast(extracted_text, analysis)

    return {
        "filename": file.filename,
        "message": "Resume uploaded and roasted!",
        "analysis": analysis,
        "roast": roast
    }


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


# Keywords a strong resume should have
important_keywords = [
    "Python", "Machine Learning", "Deep Learning", "NLP", "FastAPI",
    "Flask", "Django", "AWS", "TensorFlow", "PyTorch", "Git", "Docker"
]

# Common buzzwords that sound generic
buzzwords = [
    "hardworking", "team player", "motivated", "go-getter", "detail-oriented",
    "passionate", "dynamic", "proactive", "results-driven"
]


# Function to analyze resume text
def analyze_resume(text):
    text_lower = text.lower()

    # Check for important keywords
    found_keywords = [kw for kw in important_keywords if kw.lower() in text_lower]

    # Check for overused buzzwords
    found_buzzwords = [bw for bw in buzzwords if bw.lower() in text_lower]

    return {
        "keywords_found": found_keywords,
        "missing_keywords": [kw for kw in important_keywords if kw not in found_keywords],
        "buzzwords_found": found_buzzwords
    }


# Function to generate a funny and sarcastic roast using Google Gemini
# Function to generate a funny and sarcastic roast using Google Gemini
def generate_roast(resume_text, analysis):
    prompt = f"""
    You are a sarcastic AI that roasts resumes, but keep it **funny, playful, and light-hearted**. Avoid any harmful or inappropriate content.

    Resume (First 500 characters):  
    {resume_text[:500]}

    Roast this resume in a **funny and witty** way, while keeping it light-hearted and humorous. Think of it as playful banter with a friend—no offensive language!
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text.strip()  # Ensure there are no extra spaces


