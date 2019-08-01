import unittest

from babel.messages import Catalog

from eq_translations.schema_translation import SchemaTranslation


class TestSchemaTranslation(unittest.TestCase):
    def setUp(self):
        self.messages = [
            {
                'original': "Notice is given under section 1 of the Statistics of Trade Act 1947."
            },
            {
                'answer_id': "feeling-answer",
                'context': "Answer for: Who are you answering for??",
                'original': "Answering for this person"
            },
            {
                'answer_id': "feeling-answer",
                'context': "Answer for: Who are you answering for??",
                'original': "Answering myself"
            }
        ]

        catalog = Catalog()

        catalog.add("Notice is given under section 1 of the Statistics of Trade Act 1947.",
                    "WELSH - Notice is given under section 1 of the Statistics of Trade Act 1947.")

        catalog.add("Answering for this person",
                    "WELSH - Answering for this person",
                    auto_comments=["answer-id: feeling-answer"],
                    context="Answer for: Who are you answering for??")

        catalog.add("Answering myself",
                    "WELSH - Answering myself",
                    auto_comments=["answer-id: feeling-answer"],
                    context="Answer for: Who are you answering for??")

        self.translator = SchemaTranslation(catalog)

    def test_translate_message(self):
        result = self.translator.translate_message(self.messages[0]['original'])

        assert result == "WELSH - {}".format(self.messages[0]['original'])

    def test_translate_unknown_message(self):
        result = self.translator.translate_message('Some string')

        assert result is None

    def test_translate_context_message(self):
        result = self.translator.translate_message(self.messages[1]['original'], self.messages[1]['answer_id'])

        assert result == "WELSH - {}".format(self.messages[1]['original'])

    def test_translate_context_message_mismatch(self):
        result = self.translator.translate_message(self.messages[1]['original'], 'some-random-id')

        assert result is None

    def test_translate_context_message_failure(self):
        result = self.translator.translate_message(self.messages[1]['original'])

        assert result is None

    def test_translate_dumb_quotes(self):

        catalog = Catalog()
        catalog.add("What is 'this persons' date of birth?",
                    "Beth yw dyddiad geni 'pobl hyn'?")

        translator = SchemaTranslation(catalog)

        translated = translator.translate_message("What is 'this persons' date of birth?")

        assert translated == "Beth yw dyddiad geni ‘pobl hyn’?"
