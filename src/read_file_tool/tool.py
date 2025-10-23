import io
import pandas as pd
import PyPDF2
from docx import Document
from pptx import Presentation
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import json

def read_file(file_content: bytes, file_name: str) -> str:
    fname = file_name.lower()
    try:
        if fname.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_content))
            return df.head(10).to_json(orient="records")
        elif fname.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            pages_text = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    pages_text.append(txt)
            return "\n\n--- PAGE BREAK ---\n\n".join(pages_text).strip()
        elif fname.endswith(".docx"):
            doc = Document(io.BytesIO(file_content))
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif fname.endswith(".txt"):
            return file_content.decode("utf-8")
        elif fname.endswith(".json"):
            data = json.loads(file_content.decode("utf-8"))
            return json.dumps(data, indent=2)
        elif fname.endswith(".xlsx") or fname.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(file_content))
            return df.head(10).to_json(orient="records")
        elif fname.endswith(".pptx"):
            prs = Presentation(io.BytesIO(file_content))
            slides_text = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        slides_text.append(shape.text)
            return "\n\n--- SLIDE BREAK ---\n\n".join(slides_text).strip()
        elif fname.endswith(".html") or fname.endswith(".htm"):
            soup = BeautifulSoup(file_content, "html.parser")
            return soup.get_text(separator="\n").strip()
        elif fname.endswith(".jpg") or fname.endswith(".jpeg") or fname.endswith(".png"):
            img = Image.open(io.BytesIO(file_content))
            text = pytesseract.image_to_string(img)
            return text.strip()
        elif fname.endswith(".md"):
            return file_content.decode("utf-8")
        else:
            return "Unsupported file type. Supported: CSV, PDF, DOCX, TXT, JSON, XLSX, PPTX, HTML, JPG/PNG, MD."
    except Exception as e:
        return f"Error reading file: {str(e)}"
