import unittest

from babel.messages import Catalog

from eq_translations.schema_translation import SchemaTranslation


class TestSchemaTranslation(unittest.TestCase):
    def setUp(self):
        self.messages = [
            {
                "original": "Notice is given under section 1 of the Statistics of Trade Act 1947."
            },
            {
                "answer_id": "feeling-answer",
                "context": "Answer for: Who are you answering for??",
                "original": "Answering for this person",
            },
            {
                "answer_id": "feeling-answer",
                "context": "Answer for: Who are you answering for??",
                "original": "Answering myself",
            },
            {
                "original": (
                    "{number_of_people} person lives here, is this correct?",
                    "{number_of_people} people live here, is this correct?",
                ),
            },
            {
                "answer_id": "count-answer",
                "context": "Answer for: {number_of_people} people live here, is this correct?",
                "original": (
                    "Yes, {number_of_people} person lives here",
                    "Yes, {number_of_people} people live here",
                ),
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
            auto_comments=["answer-id: feeling-answer"],
            context="Answer for: Who are you answering for??",
        )

        catalog.add(
            id="Answering myself",
            string="WELSH - Answering myself",
            auto_comments=["answer-id: feeling-answer"],
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
            auto_comments=["answer-id: count-answer"],
            context="Answer for: {number_of_people} people live here, is this correct?",
        )

        self.translator = SchemaTranslation(catalog)

    def test_translate_non_pluralizable_message(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[0]["original"], pluralizable=False
        )

        assert result == "WELSH - {}".format(self.messages[0]["original"])

    def test_translate_pluralizable_message(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[3]["original"], pluralizable=True,
        )

        assert result == ("WELSH - one", "WELSH - other", "WELSH - many")

    def test_translate_unknown_message(self):
        result = self.translator.get_translation(
            message_id_to_translate="Some string", pluralizable=False
        )

        assert result is None

    def test_translate_non_pluralizable_message_with_context(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[1]["original"],
            answer_id=self.messages[1]["answer_id"],
            pluralizable=False,
        )

        assert result == "WELSH - {}".format(self.messages[1]["original"])

    def test_translate_pluralizable_message_with_context(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[4]["original"],
            answer_id=self.messages[4]["answer_id"],
            pluralizable=True,
        )

        assert result == ("WELSH - one", "WELSH - other", "WELSH - many")

    def test_translate_context_message_mismatch(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[1]["original"],
            answer_id="some-random-id",
            pluralizable=False,
        )

        assert result is None

    def test_translate_context_message_failure(self):
        result = self.translator.get_translation(
            message_id_to_translate=self.messages[1]["original"], pluralizable=False
        )

        assert result is None

    def test_multiple_answer_ids(self):

        catalog = Catalog()

        catalog.add(
            "Answering for this person",
            "WELSH - Answering for this person",
            auto_comments=[
                "answer-id: feeling-answer",
                "answer-id: feeling-answer-proxy",
            ],
            context="Answer for: Who are you answering for??",
        )

        translator = SchemaTranslation(catalog)

        translation_a = translator.get_translation(
            "Answering for this person", answer_id="feeling-answer", pluralizable=False
        )
        translation_b = translator.get_translation(
            "Answering for this person",
            answer_id="feeling-answer-proxy",
            pluralizable=False,
        )

        assert translation_a == "WELSH - Answering for this person"
        assert translation_b == "WELSH - Answering for this person"
