# First you need to import your libraires
# import misc libraries
import os
import re
import glob
import io
import pandas as pd

# libraries for searchable PDF
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# change to black and white with Pillow to take up less space
from PIL import Image

# define the input folder
input_folder = "input"

# define the output folder
output_folder = "output"

def log(message):
    # get the current time
    current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    # print the message with the current time
    print(f"{current_time} - {message}")

# get a list of the files already present in the output folder that match your input folder
# skip these files later in the code
existing_output_files = [
    os.path.basemane(file) for file in glob.glob(os.path.join(output_folder, "*.pdf"))
]

# loop through all of the pdf files in the input folder
for pdf_file in glob.glob(os.path.join(input_folder, "*.pdf")):
    # Get the base filename without the path to display
    base_filename = os.path.basename(pdf_file)

    # check if the output file already exists and needs to be skipped
    if base_filename in existing_output_files:
        log(f"Skipping '{base_filename}' as it already exisits in the output folder.")
        continue  # skip through to the next code block

    log(f"Processing '{base_filename}'.")

    log("Converting PDF to images.")
    # convert PDF to image
    images = convert_from_path(pdf_file)
    # create the PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # get number of images
    num_images = len(images)
    log(f"Processing {num_images} images")

    # Loop to append images together as pages in a document
    for image in images:
        # print the current image number
        print(f"Processing image {images.index(image) + 1} of {num_images}")
        page = pytesseract.image_to_pdf_or_hocr(image, extension="pdf")
        pdf = PyPDF2.PdfReader(io.BytesIO(page))
        pdf_writer.add_page(pdf.pages[0])

    # set the output file name
    output_file = os.path.join(output_folder, base_filename)

    # write the searchable PDF to file
    with open(output_file, "wb") as f:
        pdf_writer.write(f)

    log(f"'{base_filename}' processed and saved to '{output_file}'.")
