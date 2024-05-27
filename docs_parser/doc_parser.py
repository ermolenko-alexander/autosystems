from spire.doc import *
from spire.doc.common import *
from docx import Document as DC


def extract_text_from_doc(doc_path):

    document = Document()
    document.LoadFromFile(doc_path)

    document.SaveToFile("ToDocx.docx", FileFormat.Docx2016)
    document.Close()

    doc = DC("ToDocx.docx")
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    print("\n".join(text))
    return "\n".join(text)
