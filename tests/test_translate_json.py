from copy import deepcopy
import json
import unittest

from app.translate_survey import translate_survey, load_translations

input_file = "tests/test_translation_translate.xlsx"
translation_spreadsheet = load_translations(input_file)


class TranslationTests(unittest.TestCase):
    with open("tests/schemas/test_translation.json", "r") as data:
        original_json = json.load(data)
    with open("tests/schemas/test_translation_welsh.json", "r") as data:
        translated_json = json.load(data)

    def test_original_title_data(self):
        """Test that original title data is there"""
        self.assertEqual(self.original_json['title'], "Monthly Business Survey")
        self.assertEqual(self.original_json['survey_id'], "009")
        self.assertEqual(self.original_json['mime_type'], "application/json/ons/eq")
        self.assertEqual(self.original_json['theme'], "default")
        self.assertEqual(self.original_json['schema_version'], "0.0.1")
        self.assertEqual(self.original_json['data_version'], "0.0.1")
        self.assertEqual(self.original_json['legal_basis'], "StatisticsOfTradeAct")
        self.assertEqual(self.original_json['description'], "mbs_0106")

    def test_translated_title_data(self):
        """Test that title data we want / do not want to be translated is there after translation"""
        self.assertEqual(self.translated_json['title'], "Arolwg Busnes Misol")
        self.assertEqual(self.translated_json['survey_id'], "009")
        self.assertEqual(self.translated_json['legal_basis'], "StatisticsOfTradeAct")
        self.assertEqual(self.translated_json['description'], "mbs_0106")

    def test_translation_of_title_data(self):
        """When original json gets passed through function, correct title data should translate"""
        container = deepcopy(self.original_json)
        self.assertEqual(container['title'], "Monthly Business Survey")
        translate_survey(container, translation_spreadsheet)
        self.assertEqual(container['title'], "Arolwg Busnes Misol")

    def test_translation_of_section_data(self):
        """When original json gets passed through function, correct section data should translate"""
        container = deepcopy(self.original_json)
        self.assertEqual(container['sections'][0]['title'], "Navigation Title")
        translate_survey(container, translation_spreadsheet)
        self.assertEqual(container['sections'][0]['title'], "Teitl Llywio")

    def test_translation_of_group_data(self):
        """When original json gets passed through function, correct group data should translate"""
        container = deepcopy(self.original_json)
        self.assertEqual(container['sections'][1]['groups'][0]['title'], "Summary")
        translate_survey(container, translation_spreadsheet)
        self.assertEqual(container['sections'][1]['groups'][0]['title'], "Crynodeb")
