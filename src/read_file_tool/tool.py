from crewai.tools import tool
import csv
import json
import PyPDF2
import requests
from docx import Document
import tempfile
import os

@tool("read_file")
def read_file_tool(file_path: str):
    """
    Reads CSV, PDF, TXT, DOCX, and JSON files.
    Supports both local files and Google Drive links.
    """
    # --- Detect Google Drive links ---
    if "drive.google.com" in file_path:
        try:
            file_id = file_path.split("/d/")[1].split("/")[0]
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            print(f"Downloading from Google Drive: {download_url}")

            response = requests.get(download_url)
            response.raise_for_status()

            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file.write(response.content)
            tmp_file.close()

            file_path = tmp_file.name
            print(f"File downloaded to: {file_path}")

        except Exception as e:
            return f"Error downloading from Google Drive: {e}"

    # --- Regular reading logic ---
    file_type = file_path.split(".")[-1].lower() if "." in file_path else "pdf"

    try:
        if file_type == "csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [row for row in reader]

        elif file_type == "pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "".join([page.extract_text() or "" for page in reader.pages])

        elif file_type == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        elif file_type == "docx":
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])

        elif file_type == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        else:
            return f"Unsupported file type: .{file_type}"

    except Exception as e:
        return f"Error reading file: {e}"

    finally:
        if "tmp_file" in locals() and os.path.exists(tmp_file.name):
            os.unlink(tmp_file.name)
