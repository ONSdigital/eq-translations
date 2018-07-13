from copy import deepcopy
import json
import unittest

from app.extract_translation_data import get_text


class ExtractionTests(unittest.TestCase):
    with open("tests/schemas/test_translation.json", "r") as data:
        original_json = json.load(data)

    def test_extract_no_data(self):
        """Test that we get an error message if there is no data"""
        container = {"data": ""}
        with self.assertRaises(KeyError):
            get_text(container)

    def test_extract_data(self):
        """Test that correct title data gets extracted"""
        container = deepcopy(self.original_json)
        data = get_text(container)
        result = [(key, value) for (key, value) in data if key == 'description']
        self.assertEqual(data[0], result[0])
