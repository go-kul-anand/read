from tool import read_file
import os

# List of sample files to test
sample_files = [
    "sample.csv",
    "sample.pdf",
    "sample.docx",
    "sample.txt",
    "sample.json",
    "sample.xlsx",
    "sample.pptx",
    "sample.html",
    "sample.jpg",
    "sample.md"
]

for file_name in sample_files:
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            content = f.read()
        print(f"\n--- Testing {file_name} ---")
        output = read_file(content, file_name)
        # Print first 500 chars to avoid huge output
        print(output[:500] + ("..." if len(output) > 500 else ""))
    else:
        print(f"\n{file_name} not found. Please add this file to the folder to test.")
