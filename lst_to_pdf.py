import os
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF

def download_images(urls):
    images = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                images.append(img)
            else:
                print(f"Failed to download {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    return images

def save_images_to_pdf(image_urls, output_pdf_name):
    # Initialize PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add first page to PDF
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Settings for image placement
    margin = 10
    images_per_row = 4  # Number of images per row
    img_width = 50  # Width of each image
    img_height = 50  # Height of each image
    
    # Download images
    images = download_images(image_urls)
    
    x_offset = margin
    y_offset = margin
    
    # Loop through images and place them in the PDF
    for i, img in enumerate(images):
        # Save image to a temporary file
        img_temp_path = f"temp_img_{i}.jpg"
        img.save(img_temp_path)

        if x_offset + img_width > pdf.w - margin:  # If image overflows, go to the next row
            x_offset = margin
            y_offset += img_height + margin  # Add space for next row
            if y_offset + img_height > pdf.h - margin:  # If we reach the bottom, create a new page
                pdf.add_page()
                y_offset = margin
        
        # Add the image to the PDF
        pdf.image(img_temp_path, x_offset, y_offset, img_width, img_height)
        
        # Update the offset for next image
        x_offset += img_width + margin
    
    # Save the PDF
    pdf.output(output_pdf_name)
    print(f"PDF saved as {output_pdf_name}")
    if os.path.exists(output_pdf_name):
        return True
    else:
        return False


