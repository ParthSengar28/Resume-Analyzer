import PyPDF2
from docx import Document

def extract_resume_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        return "Unsupported file format."
