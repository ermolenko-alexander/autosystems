import unittest
import os
import fitz
from docx import Document
from unittest.mock import patch

from djvu_parser import parse_djvu
from doc_parser import extract_text_from_doc
from docx_parser import extract_text_from_docx
from pdf_parser import extract_text_from_pdf


class TestDJVUParser(unittest.TestCase):

    @patch("builtins.print")
    def test_parse_djvu(self, mocked_print):
        extracted_text = parse_djvu("test.djvu")
        self.assertTrue(extracted_text)
        mocked_print.assert_called()


class TestPDFTextExtraction(unittest.TestCase):

    def setUp(self):
        self.pdf_file = "test.pdf"
        with open(self.pdf_file, "w") as f:
            f.write("Test PDF content")

    def test_extract_text_from_pdf_success(self):
        extracted_text = extract_text_from_pdf(self.pdf_file)
        expected_text = "Test PDF content"

    def test_extract_text_from_pdf_exception(self):
        with self.assertRaises(Exception):
            extract_text_from_pdf("non_existent_file.pdf")


class TestDocxTextExtraction(unittest.TestCase):

    def setUp(self):
        self.docx_file = "test.docx"
        doc = Document()
        doc.add_paragraph("Test Docx content")
        doc.save(self.docx_file)

    @patch("builtins.print")
    def test_extract_text_from_docx_success(self, mocked_print):
        extracted_text = extract_text_from_docx(self.docx_file)
        expected_text = "Test Docx content"
        self.assertEqual(extracted_text, expected_text)
        mocked_print.assert_called()

    @patch("builtins.print")
    def test_extract_text_from_docx_exception(self, mocked_print):
        non_existent_file = "non_existent_file.docx"
        extract_text_from_docx(non_existent_file)
        mocked_print.assert_called_with(
            "Ошибка: Package not found at 'non_existent_file.docx', Возможно, файл не найден."
        )


class TestDocTextExtraction(unittest.TestCase):

    def setUp(self):
        self.test_doc_content = "Текст для проверки."
        self.doc_file = "test.doc"
        with open(self.doc_file, "w") as f:
            f.write(self.test_doc_content)

    @patch("builtins.print")
    def test_extract_text_from_doc(self, mocked_print):
        extracted_text = extract_text_from_doc(self.doc_file)

        expected_text = "Текст для проверки."
        if expected_text in extracted_text:
            mocked_print.assert_called()


class TestPDFTextExtraction(unittest.TestCase):

    def setUp(self):
        self.pdf_file = "test.pdf"
        self.pdf_content = "Test PDF content\n"

        # Создаем временный PDF файл для тестирования
        pdf_document = fitz.open()
        pdf_page = pdf_document.new_page()
        pdf_page.insert_text((100, 100), self.pdf_content)
        pdf_document.save(self.pdf_file)
        pdf_document.close()

    @patch("builtins.print")
    def test_extract_text_from_pdf_success(self, mocked_print):
        extracted_text = extract_text_from_pdf(self.pdf_file)
        self.assertEqual(extracted_text, self.pdf_content)
        mocked_print.assert_not_called()

    @patch("builtins.print")
    def test_extract_text_from_pdf_exception(self, mocked_print):
        non_existent_file = "non_existent_file.pdf"
        extracted_text = extract_text_from_pdf(non_existent_file)
        self.assertEqual(extracted_text, None)
        mocked_print.assert_called_with(
            "Ошибка: no such file: 'non_existent_file.pdf', файл, возможно, отсутствует"
        )


if __name__ == "__main__":
    unittest.main()
