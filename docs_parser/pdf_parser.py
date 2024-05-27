import fitz


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        num_pages = pdf_document.page_count
        for i in range(num_pages):
            page = pdf_document[i]
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Ошибка: {str(e)}, файл, возможно, отсутствует")
