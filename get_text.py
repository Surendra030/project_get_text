import subprocess
import sys
from mega import Mega
import os

# Define input and output file names
pdf_file = "temp.pdf"
txt_file = "output.txt"

# Run pdftotext command using subprocess
try:
    result = subprocess.run(["pdftotext", pdf_file, txt_file], capture_output=True, text=True, check=True)

    # Print extracted text to GitHub Actions logs
    with open(txt_file, "r", encoding="utf-8") as file:
        text = file.read()
        sys.stdout.write(text)  # Prints text to logs

except subprocess.CalledProcessError as e:
    sys.stderr.write(f"Error extracting text: {e}\n")

if os.path.exists(txt_file):
    mega = Mega()
    m = mega.login('afg154006@gmail.com','megaMac02335!')
    m.upload(txt_file)
else:
    print("file not found..")
    