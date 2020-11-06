from babel import Locale
from babel.messages import Catalog

from eq_translations import SchemaTranslation, SurveySchema
from eq_translations.translatable_item import TranslatableItem


def test_translate():
    schema_translation = SchemaTranslation()

    catalog = Catalog(locale=Locale("cy"))

    catalog.add(
        "Answering for this person",
        "WELSH - Answering for this person",
        context="Who are you answering for??",
    )

    catalog.add(
        "Answering myself",
        "WELSH - Answering myself",
        context="Who are you answering for??",
    )

    schema_translation.catalog = catalog

    schema = SurveySchema(
        {
            "blocks": [
                {
                    "question": {
                        "title": "Who are you answering for??",
                        "description": "",
                        "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                        "answers": [
                            {
                                "type": "Radio",
                                "id": "feeling-answer",
                                "label": "Feeling answer",
                                "mandatory": True,
                                "options": [
                                    {
                                        "label": "Answering for this person",
                                        "value": "good",
                                    },
                                    {
                                        "label": "Answering myself",
                                        "value": "bad",
                                        "detail_answer": {
                                            "id": "feeling-bad-answer",
                                            "label": "Specify why answering for yourself is bad",
                                            "mandatory": True,
                                            "type": "TextField",
                                        },
                                    },
                                ],
                                "guidance": {
                                    "hide_guidance": "Hide feeling answer help",
                                    "show_guidance": "Show feeling answer help",
                                    "contents": [
                                        {
                                            "title": "Feeling answer",
                                            "description": "This should be answered to see if you are answering on behalf of someone else",
                                        }
                                    ],
                                },
                            }
                        ],
                    }
                }
            ]
        }
    )
    translated = schema.translate(schema_translation)

    expected = {
        "blocks": [
            {
                "question": {
                    "title": "Who are you answering for??",
                    "description": "",
                    "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                    "answers": [
                        {
                            "type": "Radio",
                            "id": "feeling-answer",
                            "label": "Feeling answer",
                            "mandatory": True,
                            "options": [
                                {
                                    "label": "WELSH - Answering for this person",
                                    "value": "good",
                                },
                                {
                                    "label": "WELSH - Answering myself",
                                    "value": "bad",
                                    "detail_answer": {
                                        "id": "feeling-bad-answer",
                                        "label": "Specify why answering for yourself is bad",
                                        "mandatory": True,
                                        "type": "TextField",
                                    },
                                },
                            ],
                            "guidance": {
                                "hide_guidance": "Hide feeling answer help",
                                "show_guidance": "Show feeling answer help",
                                "contents": [
                                    {
                                        "title": "Feeling answer",
                                        "description": "This should be answered to see if you are answering on behalf of someone else",
                                    }
                                ],
                            },
                        }
                    ],
                }
            },
        ],
        "language": "cy",
    }

    assert expected == translated.schema


def test_get_catalog():
    schema_data = {
        "sections": [
            {
                "question": {
                    "title": "Please confirm the number of people who live at this household",
                    "description": "",
                    "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                    "answers": [
                        {
                            "type": "Radio",
                            "id": "live-here-answer",
                            "label": "Live here answer",
                            "mandatory": True,
                            "options": [
                                {
                                    "label": {
                                        "text_plural": {
                                            "forms": {
                                                "one": "{number_of_people} person lives here",
                                                "other": "{number_of_people} people live here",
                                            },
                                            "count": {
                                                "source": "answers",
                                                "identifier": "number-of-people-answer",
                                            },
                                        },
                                        "placeholders": [
                                            {
                                                "placeholder": "number_of_people",
                                                "value": {
                                                    "source": "answers",
                                                    "identifier": "number-of-people-answer",
                                                },
                                            }
                                        ],
                                    }
                                },
                                {
                                    "label": "No, I need to change my answer",
                                    "value": "No, I need to change my answer",
                                    "detail_answer": {
                                        "id": "feeling-bad-answer",
                                        "label": "Enter a reason why",
                                        "mandatory": True,
                                        "type": "TextField",
                                    },
                                },
                            ],
                            "guidance": {
                                "hide_guidance": "Hide feeling answer help",
                                "show_guidance": "Show feeling answer help",
                                "contents": [
                                    {
                                        "title": "Feeling answer",
                                        "description": "This should be answered to see if you are answering on behalf of someone else",
                                    }
                                ],
                            },
                        }
                    ],
                }
            }
        ]
    }

    schema = SurveySchema(schema_data)
    catalog = schema.catalog

    actual_items = [message.id for message in catalog]

    assert schema_data["sections"][0]["question"]["title"] in actual_items
    assert schema_data["sections"][0]["question"]["answers"][0]["label"] in actual_items
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["options"][1]["label"]
        in actual_items
    )
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["options"][1][
            "detail_answer"
        ]["label"]
        in actual_items
    )
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["guidance"][
            "hide_guidance"
        ]
        in actual_items
    )
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["guidance"][
            "show_guidance"
        ]
        in actual_items
    )
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["guidance"]["contents"][0][
            "title"
        ]
        in actual_items
    )
    assert (
        schema_data["sections"][0]["question"]["answers"][0]["guidance"]["contents"][0][
            "description"
        ]
        in actual_items
    )
    assert schema_data["sections"][0]["question"]["instruction"] in actual_items

    singular = schema_data["sections"][0]["question"]["answers"][0]["options"][0][
        "label"
    ]["text_plural"]["forms"]["one"]
    plural_label = schema_data["sections"][0]["question"]["answers"][0]["options"][0][
        "label"
    ]["text_plural"]["forms"]["other"]

    assert (singular, plural_label) in actual_items


def test_get_placeholder_pointers(schema_with_placeholders):
    schema = SurveySchema(schema_with_placeholders)
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/label/text",
            description="Answer option",
            value="{address}",
            context="During term time, where does <em>{person_name}</em> usually live?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/1/label/text",
            description="Answer option",
            value="The address in {country}",
            context="During term time, where does <em>{person_name}</em> usually live?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/title/text",
            description="Question text",
            value="During term time, where does <em>{person_name}</em> usually live?",
        )
        in translatable_items
    )


def test_placeholder_catalog_context(schema_with_placeholders):
    schema = SurveySchema(schema_with_placeholders)

    message = schema.catalog.get(
        id="{address}",
        context="During term time, where does <em>{person_name}</em> usually live?",
    )
    assert (
        message.context
        == "During term time, where does <em>{person_name}</em> usually live?"
    )


def test_placeholder_translation(schema_with_placeholders):
    schema_translation = SchemaTranslation()

    catalog = Catalog(locale=Locale("cy"))

    catalog.add(
        id="During term time, where does <em>{person_name}</em> usually live?",
        string="WELSH - During term time, where does <em>{person_name}</em> usually live?",
    )

    catalog.add(
        id="{address}",
        string="WELSH - {address}",
        context="During term time, where does <em>{person_name}</em> usually live?",
    )

    catalog.add(
        id="The address in {country}",
        string="WELSH - The address in {country}",
        context="During term time, where does <em>{person_name}</em> usually live?",
    )

    schema_translation.catalog = catalog

    schema = SurveySchema(schema_with_placeholders)
    translated = schema.translate(schema_translation)

    expected = {
        "question": {
            "id": "term-time-location-question",
            "type": "General",
            "title": {
                "placeholders": [
                    {
                        "placeholder": "person_name",
                        "transforms": [
                            {
                                "arguments": {
                                    "delimiter": " ",
                                    "list_to_concatenate": {
                                        "identifier": ["first-name", "last-name",],
                                        "source": "answers",
                                    },
                                },
                                "transform": "concatenate_list",
                            }
                        ],
                    }
                ],
                "text": "WELSH - During term time, where does <em>{person_name}</em> usually live?",
            },
            "answers": [
                {
                    "id": "term-time-location-answer",
                    "mandatory": True,
                    "options": [
                        {
                            "label": {
                                "placeholders": [
                                    {
                                        "placeholder": "address",
                                        "value": {
                                            "identifier": "display_address",
                                            "source": "metadata",
                                        },
                                    }
                                ],
                                "text": "WELSH - {address}",
                            },
                            "value": "household-address",
                        },
                        {
                            "label": {
                                "placeholders": [
                                    {
                                        "placeholder": "country",
                                        "value": {
                                            "identifier": "another-address-answer-other-country",
                                            "source": "answers",
                                        },
                                    }
                                ],
                                "text": "WELSH - The address in {country}",
                            },
                            "value": "30-day-address",
                        },
                    ],
                    "type": "Radio",
                }
            ],
        },
        "language": "cy",
    }

    assert expected == translated.schema


def test_variant_translation(schema_with_question_variants):
    schema_translation = SchemaTranslation()

    catalog = Catalog()

    catalog.add(
        "First name", "WELSH - First name", context="What is your name?",
    )

    catalog.add(
        "First name", "WELSH - First name - Proxy", context="What is their name?",
    )

    schema_translation.catalog = catalog

    variant_schema = SurveySchema(schema_with_question_variants)

    translated = variant_schema.translate(schema_translation)

    assert (
        translated.schema["question_variants"][0]["question"]["answers"][0]["label"]
        == "WELSH - First name"
    )
    assert (
        translated.schema["question_variants"][1]["question"]["answers"][0]["label"]
        == "WELSH - First name - Proxy"
    )


def test_plural_translation(schema_with_plurals):
    schema_translation = SchemaTranslation()

    catalog = Catalog(locale=Locale("cy"))

    catalog.add(
        id=(
            "{number_of_people} person lives here, is this correct?",
            "{number_of_people} people live here, is this correct?",
        ),
        string=(
            "WELSH - zero",
            "WELSH - one",
            "WELSH - two",
            "WELSH - few",
            "WELSH - many",
            "WELSH - other",
        ),
    )

    catalog.add(
        id=(
            "Yes, {number_of_people} person lives here",
            "Yes, {number_of_people} people live here",
        ),
        string=(
            "WELSH - zero",
            "WELSH - one",
            "WELSH - two",
            "WELSH - few",
            "WELSH - many",
            "WELSH - other",
        ),
        context="{number_of_people} people live here, is this correct?",
    )

    schema_translation.catalog = catalog

    plural_forms_schema = SurveySchema(schema_with_plurals)

    translated = plural_forms_schema.translate(schema_translation)

    forms_for_title = translated.schema["question"]["title"]["text_plural"]["forms"]

    assert forms_for_title["zero"] == "WELSH - zero"
    assert forms_for_title["one"] == "WELSH - one"
    assert forms_for_title["two"] == "WELSH - two"
    assert forms_for_title["few"] == "WELSH - few"
    assert forms_for_title["many"] == "WELSH - many"
    assert forms_for_title["other"] == "WELSH - other"

    forms_for_answer_label = translated.schema["question"]["answers"][0]["options"][0][
        "label"
    ]["text_plural"]["forms"]

    assert forms_for_answer_label["zero"] == "WELSH - zero"
    assert forms_for_answer_label["one"] == "WELSH - one"
    assert forms_for_answer_label["two"] == "WELSH - two"
    assert forms_for_answer_label["few"] == "WELSH - few"
    assert forms_for_answer_label["many"] == "WELSH - many"
    assert forms_for_answer_label["other"] == "WELSH - other"


def test_translate_sets_language():
    catalog = Catalog(locale=Locale("cy"))
    catalog.add("test")

    schema_translation = SchemaTranslation(catalog=catalog)

    schema = SurveySchema({})
    schema.translate(schema_translation)

    translated_schema = schema.translate(schema_translation)

    assert translated_schema.language == "cy"


def test_locale_on_load_welsh():
    translation = SchemaTranslation()
    translation.load("tests/schemas/test_language-cy.po")

    assert translation.language == "cy"


def test_locale_on_load_ulster_scots():
    translation = SchemaTranslation()
    translation.load("tests/schemas/test_language-eo.po")

    assert translation.language == "eo"


def test_checkbox_null_label():

    schema_translation = SchemaTranslation()
    catalog = Catalog(locale=Locale("cy"))
    catalog.add(
        "Rugby", "Rygbi",
    )
    schema_translation.catalog = catalog
    schema = SurveySchema(
        {
            "question": {
                "answers": [
                    {"label": None, "options": [{"label": "Rugby", "value": "Rugby"}]}
                ],
            }
        }
    )
    translated = schema.translate(schema_translation)
    expected = {
        "question": {
            "answers": [
                {"label": None, "options": [{"label": "Rygbi", "value": "Rugby"},],}
            ],
        },
        "language": "cy",
    }
    assert expected == translated.schema
