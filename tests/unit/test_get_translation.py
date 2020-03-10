import unittest

from babel.messages import Catalog

from eq_translations.schema_translation import SchemaTranslation


class TestGetTranslation(unittest.TestCase):
    def setUp(self):
        self.messages = [
            {
                "original": "Notice is given under section 1 of the Statistics of Trade Act 1947."
            },
            {
                "original": "Answering for this person",
                "context": "Answer for: Who are you answering for??",
            },
            {
                "original": "Answering myself",
                "context": "Answer for: Who are you answering for??",
            },
            {
                "original": (
                    "{number_of_people} person lives here, is this correct?",
                    "{number_of_people} people live here, is this correct?",
                ),
            },
            {
                "original": (
                    "Yes, {number_of_people} person lives here",
                    "Yes, {number_of_people} people live here",
                ),
                "context": "Answer for: {number_of_people} people live here, is this correct?",
            },
        ]

        catalog = Catalog()

        catalog.add(
            id="Notice is given under section 1 of the Statistics of Trade Act 1947.",
            string="WELSH - Notice is given under section 1 of the Statistics of Trade Act 1947.",
        )

        catalog.add(
            id="Answering for this person",
            string="WELSH - Answering for this person",
            context="Answer for: Who are you answering for??",
        )

        catalog.add(
            id="Answering myself",
            string="WELSH - Answering myself",
            context="Answer for: Who are you answering for??",
        )

        catalog.add(
            id=(
                "{number_of_people} person lives here, is this correct?",
                "{number_of_people} people live here, is this correct?",
            ),
            string=("WELSH - one", "WELSH - other", "WELSH - many"),
        )

        catalog.add(
            id=(
                "Yes, {number_of_people} person lives here",
                "Yes, {number_of_people} people live here",
            ),
            string=("WELSH - one", "WELSH - other", "WELSH - many"),
            context="Answer for: {number_of_people} people live here, is this correct?",
        )

        self.translator = SchemaTranslation(catalog)

    def test_translate_unknown_message(self):
        result = self.translator.get_translation(message_id="Some string")

        assert result is None

    def test_translate_non_pluralizable_message(self):
        result = self.translator.get_translation(
            message_id=self.messages[0]["original"]
        )

        assert result == f"WELSH - {self.messages[0]['original']}"

    def test_translate_pluralizable_message(self):
        result = self.translator.get_translation(
            message_id=self.messages[3]["original"]
        )

        assert result == ("WELSH - one", "WELSH - other", "WELSH - many")

    def test_translate_non_pluralizable_message_with_context(self):
        result = self.translator.get_translation(
            message_id=self.messages[1]["original"],
            message_context=self.messages[1]["context"],
        )

        assert result == f"WELSH - {self.messages[1]['original']}"

    def test_translate_pluralizable_message_with_context(self):
        result = self.translator.get_translation(
            message_id=self.messages[4]["original"],
            message_context=self.messages[4]["context"],
        )

        assert result == ("WELSH - one", "WELSH - other", "WELSH - many")

    def test_translate_context_message_mismatch(self):
        result = self.translator.get_translation(
            message_id=self.messages[1]["original"],
            message_context="some-random-context",
        )

        assert result is None

    def test_translate_context_message_with_no_context(self):
        result = self.translator.get_translation(
            message_id=self.messages[1]["original"], message_context=None
        )

        assert result is None
