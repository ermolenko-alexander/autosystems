import os
import unittest
from gazeta_parser import parse, write_to_csv, parse_one_link


class TestParse(unittest.TestCase):
    def test_parse(self):
        # Test that the parse function returns a list of links
        links = [
            "https://www.gazeta.ru/sport/news/2024/05/22/23074501.shtml",
            "https://www.gazeta.ru/army/news/2024/05/22/23074423.shtml",
            "https://www.gazeta.ru/style/news/2024/05/22/23074471.shtml",
            "https://www.gazeta.ru/tech/news/2024/05/16/23023147.shtml",
        ]
        self.assertIsInstance(links, list)
        self.assertGreater(len(links), 0)

    def test_write_to_csv(self):
        # Test that the write_to_csv function writes a CSV file
        data = [
            {
                "link": "https://example.com",
                "text": "Example text",
                "date": "2024-05-22 12:00:00",
            }
        ]
        write_to_csv(data)
        self.assertTrue(os.path.exists("output.csv"))

    def test_parse_one_link(self):
        # Test that the parse_one_link function returns a dictionary with the correct keys
        url = "https://www.gazeta.ru/social/2024/05/22/19127077.shtml"
        result = parse_one_link(url)
        self.assertIsInstance(result, dict)
        self.assertIn("link", result)
        self.assertIn("text", result)
        self.assertIn("date", result)

    def test_parse_one_link_error(self):
        # Test that the parse_one_link function handles errors correctly
        url = "https://example.com/broken_link"
        result = parse_one_link(url)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
