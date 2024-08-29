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

# define paths

# poppler_path will be mapped to a libaray/bin
poppler_path = "/opt/homebrew/Cellar/poppler/24.04.0_1/bin"

# pytesseract will be mapped to an .exe
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# define the input folder
input_folder = "input"

# define the output folder
output_folder = "output"


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
        print(f"Skipping '{base_filename}' as it already exisits in the output folder.")
        continue  # skip through to the next code block

    # convert PDF to image
    images = convert_from_path(pdf_file, poppler_path=poppler_path)

    # create the PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Loop to append images together as pages in a document
    for image in images:
        page = pytesseract.image_to_pdf_or_hocr(image, extension="pdf")
        pdf = PyPDF2.PdfReader(io.BytesIO(page))
        pdf_writer.add_page(pdf.pages[0])

    # set the output file name
    output_file = os.path.join(output_folder, base_filename)

    # write the searchable PDF to file
    with open(output_file, "wb") as f:
        pdf_writer.write(f)

    print(f"'{base_filename}' processed and saved to '{output_file}'.")
