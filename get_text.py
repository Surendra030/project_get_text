import subprocess
import sys
from mega import Mega
import os
import json
from lst_to_pdf import save_images_to_pdf

# Define input and output file names
pdf_file = "temp.pdf"
txt_file = f"{pdf_file.split(".")[0]}.txt"

# img_lst_url = []
# with open('json_lst.json',encoding='utf-8')as f:
#     img_lst_url = json.load(f)

# # Call the function to download images and save them to a PDF
# flag = save_images_to_pdf(img_lst_url, pdf_file)

if os.path.exists(pdf_file):
        
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
        keys = os.getenv("M_TOKEN").split("_")
        
        mega = Mega()
        m = mega.login(keys[0],keys[1])
        m.upload(txt_file)
    else:
        print("file not found..")
else:
    print("url to pdf conversion failed..")