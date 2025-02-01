import subprocess
import sys
import os
import json
from mega import Mega
import shutil

# Define input and output file names
pdf_file = "temp.pdf"
txt_file = f"{pdf_file.split('.')[0]}.json"

# Check if pdftotext is installed
if shutil.which("pdftotext") is None:
    print("pdftotext is not installed.")
    sys.exit(1)

if os.path.exists(pdf_file):
    temp = []
    # Run pdftotext command using subprocess
    try:
        result = subprocess.run(["pdftotext", pdf_file, txt_file], capture_output=True, text=True, check=True)
        temp.append(result.stdout)  # Use stdout instead of the full result object
        # Print extracted text to GitHub Actions logs
        with open(txt_file, "w", encoding="utf-8") as file:
            json.dump(temp, file, indent=4)

    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error extracting text: {e}\n")

    if os.path.exists(txt_file) and os.path.getsize(txt_file) > 0:
        keys = os.getenv("M_TOKEN")
        if keys:
            keys = keys.split("_")
            mega = Mega()
            m = mega.login(keys[0], keys[1])
            m.upload(txt_file)
        else:
            print("M_TOKEN environment variable is not set.")
    else:
        print("Text extraction failed or file is empty.")
else:
    print("PDF file not found.")
