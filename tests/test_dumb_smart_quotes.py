import unittest

from eq_translations.utils import dumb_to_smart_quotes


class TestDumbToSmartQuotes(unittest.TestCase):

    def test_dumb_to_smart_quotes_welsh_single(self):
        original_text = '''sy'n ymweld â'r Deyrnas Unedig'''
        expected = '''sy’n ymweld â’r Deyrnas Unedig'''

        actual = dumb_to_smart_quotes(original_text)

        self.assertNotEqual(actual, original_text)
        self.assertEqual(actual, expected)

    def test_dumb_to_smart_quotes_english_single(self):
        original_text = '''you're sure he'd said that 'quoting a few words' gave 'smart' quotes?'''
        expected = '''you’re sure he’d said that ‘quoting a few words’ gave ‘smart’ quotes?'''

        actual = dumb_to_smart_quotes(original_text)

        self.assertNotEqual(actual, original_text)
        self.assertEqual(actual, expected)

    @unittest.expectedFailure
    def test_dumb_to_smart_quotes_english_double(self):
        # Double quotes not supported yet...
        original_text = '''here is "a sentence with" double dumb "quotes" in the middle'''
        expected = '''here is “a sentence with” double dumb “quotes” in the middle'''

        actual = dumb_to_smart_quotes(original_text)

        self.assertNotEqual(actual, original_text)
        self.assertEqual(actual, expected)

