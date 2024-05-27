from docx import Document


def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        print("\n".join(text))
        return "\n".join(text)
    except Exception as err:
        print(f"Ошибка: {err}, Возможно, файл не найден.")
