import unittest
from app.template_extractor import TemplateExtractor


class TranslationTests(unittest.TestCase):

    def setUp(self):
        self.schema_path = "./tests/schemas/test_translation.json"

    def test_extract_translation_pot(self):
        output_directory = "./tests/output/pot-files"

        template_extractor = TemplateExtractor(self.schema_path)
        template_extractor.save(output_directory)

        line_count = 0
        msgid_count = 0
        pot_file = "./tests/output/pot-files/test_translation.pot"
        with open(pot_file) as f:
            for line in f:
                line_count += 1
                if line.startswith('msgid'):
                    msgid_count += 1

        self.assertEqual(line_count, 170)
        self.assertEqual(msgid_count, 50)
