import subprocess
import fitz
import os
import pytesseract
from PIL import Image


def convert_djvu_to_pdf(djvu_file_path, pdf_file_path):
    process = subprocess.Popen(
        ["ddjvu", "-format=pdf", "-quality=85", djvu_file_path, pdf_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    if stderr:
        print(f"Ошибка конвертирования: {stderr.decode('utf-8')}")


def convert_pdf_to_images(pdf_file):
    doc = fitz.open(pdf_file)

    tmp_img_dir = "tmp_images"
    if not os.path.exists(tmp_img_dir):
        os.makedirs(tmp_img_dir)

    image_paths = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_path = f"{tmp_img_dir}/page_{page_num}.png"
        image_paths.append(image_path)

        pixmap = page.get_pixmap()

        img_data = pixmap.samples

        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], img_data)
        image.save(image_path)

    doc.close()

    return image_paths


def extract_text_from_images(image_paths):
    extracted_text = ""

    for image_path in image_paths:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        extracted_text += text

    return extracted_text


def parse_djvu(filename):

    djvu_file_path = filename
    pdf_file_path = "converted.pdf"

    convert_djvu_to_pdf(djvu_file_path, pdf_file_path)

    pdf_file = "converted.pdf"

    image_paths = convert_pdf_to_images(pdf_file)

    extracted_text = extract_text_from_images(image_paths)

    print(extracted_text)

    for image_path in image_paths:
        os.remove(image_path)

    os.rmdir("tmp_images")

    return extracted_text
