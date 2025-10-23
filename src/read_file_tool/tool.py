from crewai.tools.tool import Tool
import csv
import json
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import openpyxl
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract


class ReadFileTool(Tool):
    """
    A CrewAI Tool to read multiple file types:
    CSV, PDF, DOCX, TXT, JSON, XLSX, PPTX, HTML, JPG/PNG, MD
    """

    def read_file(self, file_path: str):
        file_path = Path(file_path)
        if not file_path.exists():
            return f"{file_path.name} not found. Please add this file to the folder to test."

        suffix = file_path.suffix.lower()

        try:
            if suffix == ".csv":
                with open(file_path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    return [row for row in reader]

            elif suffix == ".pdf":
                reader = PdfReader(str(file_path))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()

            elif suffix == ".docx":
                doc = Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])

            elif suffix == ".txt" or suffix == ".md":
                return file_path.read_text(encoding="utf-8")

            elif suffix == ".json":
                return json.loads(file_path.read_text(encoding="utf-8"))

            elif suffix == ".xlsx":
                wb = openpyxl.load_workbook(file_path)
                data = {}
                for sheet in wb.sheetnames:
                    ws = wb[sheet]
                    data[sheet] = [[cell.value for cell in row] for row in ws.iter_rows()]
                return data

            elif suffix == ".pptx":
                prs = Presentation(file_path)
                slides_text = []
                for slide in prs.slides:
                    slide_text = []
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            slide_text.append(shape.text)
                    slides_text.append("\n".join(slide_text))
                return slides_text

            elif suffix == ".html":
                html_content = file_path.read_text(encoding="utf-8")
                soup = BeautifulSoup(html_content, "html.parser")
                return soup.get_text()

            elif suffix in [".jpg", ".jpeg", ".png"]:
                img = Image.open(file_path)
                return pytesseract.image_to_string(img)

            else:
                return f"Unsupported file type: {suffix}"

        except Exception as e:
            return f"Error reading file: {str(e)}"
