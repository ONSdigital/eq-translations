import unittest

from babel.messages import Catalog

from eq_translations.schema_translation import SchemaTranslation
from eq_translations.survey_schema import SurveySchema


class TestSurveySchema(unittest.TestCase):
    LANGUAGE_CODE = "cy"

    VARIANT_SCHEMA = {
        "id": "name",
        "question_variants": [
            {
                "question": {
                    "answers": [
                        {
                            "id": "first-name",
                            "label": "First name",
                            "mandatory": True,
                            "type": "TextField",
                            "validation": {
                                "messages": {
                                    "MANDATORY_TEXTFIELD": "Please enter a name or remove the person to continue"
                                }
                            },
                        },
                        {
                            "id": "last-name",
                            "label": "Last name",
                            "mandatory": False,
                            "type": "TextField",
                        },
                    ],
                    "id": "name-question",
                    "title": "What is your name?",
                    "type": "General",
                }
            },
            {
                "question": {
                    "answers": [
                        {
                            "id": "first-name",
                            "label": "First name",
                            "mandatory": True,
                            "type": "TextField",
                            "validation": {
                                "messages": {
                                    "MANDATORY_TEXTFIELD": "Please enter a name or remove the person to continue"
                                }
                            },
                        },
                        {
                            "id": "last-name",
                            "label": "Last name",
                            "mandatory": False,
                            "type": "TextField",
                        },
                    ],
                    "id": "name-question",
                    "title": "What is their name?",
                    "type": "General",
                }
            },
        ],
        "type": "Question",
    }

    PLURAL_FORMS_SCHEMA = {
        "id": "name",
        "type": "Question",
        "question": {
            "type": "General",
            "id": "total-people-question",
            "title": {
                "text_plural": {
                    "forms": {
                        "one": "{number_of_people} person lives here, is this correct?",
                        "other": "{number_of_people} people live here, is this correct?",
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
            },
            "answers": [
                {
                    "id": "confirm-count",
                    "mandatory": True,
                    "type": "Radio",
                    "options": [
                        {
                            "label": {
                                "text_plural": {
                                    "forms": {
                                        "one": "Yes, {number_of_people} person lives here",
                                        "other": "Yes, {number_of_people} people live here",
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
                            },
                            "value": "Yes",
                        },
                        {"label": "No", "value": "No"},
                    ],
                }
            ],
        },
    }

    def test_find_variant_pointers(self):
        schema = SurveySchema(TestSurveySchema.VARIANT_SCHEMA)

        pointers = schema.get_title_pointers()

        assert "/question_variants/0/question/title" in pointers
        assert "/question_variants/1/question/title" in pointers

    def test_get_messages(self):
        schema = SurveySchema()
        schema.load("./tests/schemas/en/test_translation.json")

        assert schema.pointers is not None

    def test_get_titles_messages(self):
        schema = SurveySchema(
            {
                "sections": [
                    {
                        "type": "CalculatedSummary",
                        "id": "block-3",
                        "title": "Calculated Summary Main Title Block 2",
                        "calculation": {
                            "calculation_type": "sum",
                            "answers_to_calculate": [
                                "first-number-answer",
                                "second-number-answer",
                            ],
                            "title": "Calculated Summary Calculation Title Block 2",
                        },
                    }
                ]
            }
        )
        pointers = schema.get_title_pointers()
        assert "/sections/0/title" in pointers
        assert "/sections/0/calculation/title" in pointers

        assert len(pointers) == 2

    def test_get_list_messages(self):
        schema = SurveySchema(
            {
                "sections": [
                    {
                        "content": [
                            {
                                "title": "Include:",
                                "list": [
                                    "all employees in Great Britain (England, Scotland and Wales), both full and part-time, who received pay in the relevant period"
                                ],
                            },
                            {
                                "title": "Exclude:",
                                "list": [
                                    "trainees on government schemes",
                                    "employees working abroad unless paid directly from this business’s GB payroll",
                                    "employees in Northern Ireland",
                                ],
                            },
                        ]
                    }
                ]
            }
        )

        pointers = schema.get_list_pointers()

        assert "/sections/0/content/0/list/0" in pointers
        assert "/sections/0/content/1/list/0" in pointers
        assert "/sections/0/content/1/list/1" in pointers
        assert "/sections/0/content/1/list/2" in pointers

        assert len(pointers) == 4

    def test_no_pointers_when_list_property_is_not_a_list(self):
        schema = SurveySchema({"list": "abc"})
        pointers = schema.get_list_pointers()
        assert "/list" not in pointers
        assert "/list/0" not in pointers
        assert "/list/1" not in pointers
        assert "/list/2" not in pointers

    def test_get_answer_messages(self):
        schema = SurveySchema(
            {
                "sections": [
                    {
                        "question": [
                            {
                                "answers": [
                                    {
                                        "id": "confirm-feeling-answer",
                                        "type": "Radio",
                                        "label": "confirm",
                                        "mandatory": True,
                                        "options": [
                                            {"value": "Yes", "label": "Yes"},
                                            {"value": "No", "label": "No"},
                                        ],
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

        pointers = schema.get_answer_pointers()

        assert "/sections/0/question/0/answers/0/options/0/label" in pointers
        assert "/sections/0/question/0/answers/0/options/1/label" in pointers

    def test_get_all_pointers(self):
        schema = SurveySchema(
            {
                "sections": [
                    {
                        "content": [
                            {
                                "title": "Include:",
                                "list": [
                                    "all employees in Great Britain (England, Scotland and Wales), both full and part-time, who received pay in the relevant period"
                                ],
                            },
                            {
                                "title": "Exclude:",
                                "list": [
                                    "trainees on government schemes",
                                    "employees working abroad unless paid directly from this business’s GB payroll",
                                    "employees in Northern Ireland",
                                ],
                            },
                        ]
                    }
                ]
            }
        )

        assert "/sections/0/content/0/title" in schema.pointers
        assert "/sections/0/content/1/title" in schema.pointers
        assert "/sections/0/content/0/list/0" in schema.pointers
        assert "/sections/0/content/1/list/0" in schema.pointers
        assert "/sections/0/content/1/list/1" in schema.pointers
        assert "/sections/0/content/1/list/2" in schema.pointers

        assert len(schema.pointers) == 6

    def test_get_parent_id(self):
        schema = SurveySchema(
            {
                "sections": [
                    {
                        "question": {
                            "answers": [
                                {
                                    "id": "confirm-feeling-answer",
                                    "type": "Radio",
                                    "label": "confirm",
                                    "mandatory": True,
                                    "options": [
                                        {"value": "Yes", "label": "Yes"},
                                        {"value": "No", "label": "No"},
                                    ],
                                }
                            ]
                        }
                    }
                ]
            }
        )

        option_parent_id = schema.get_parent_id(
            "/sections/0/question/answers/0/options/0/label"
        )
        answer_parent_id = schema.get_parent_id("/sections/0/question/answers/0/label")

        assert option_parent_id == "confirm-feeling-answer"
        assert answer_parent_id == "confirm-feeling-answer"

    def test_get_parent_question_pointer(self):
        schema = SurveySchema()
        parent_question_pointer = schema.get_parent_question_pointer(
            "/question/0/answers/0/options/0/label"
        )

        assert parent_question_pointer == "/question"

    def test_get_parent_question(self):
        original_question = {
            "question": {
                "answers": [
                    {
                        "id": "confirm-feeling-answer",
                        "type": "Radio",
                        "label": "confirm",
                        "mandatory": True,
                        "options": [
                            {"value": "Yes", "label": "Yes"},
                            {"value": "No", "label": "No"},
                        ],
                    }
                ]
            },
            "title": "text",
        }

        schema = SurveySchema({"question": original_question})
        parent_question = schema.get_parent_question(
            "/question/0/answers/0/options/0/label"
        )
        assert parent_question == original_question["title"]

    def test_relationship_playback_extraction(self):
        relationships_question = {
            "question": {
                "id": "relationship-question",
                "type": "General",
                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
                "answers": [
                    {
                        "id": "relationship-answer",
                        "mandatory": True,
                        "type": "Relationship",
                        "playback": "{second_person_name} is {first_person_name_possessive} <em>…</em>",
                        "options": [
                            {
                                "label": "Husband or Wife",
                                "value": "Husband or Wife",
                                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>",
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>",
                            },
                            {
                                "label": "Legally registered civil partner",
                                "value": "Legally registered civil partner",
                                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>",
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>",
                            },
                            {
                                "label": "Son or daughter",
                                "value": "Son or daughter",
                                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>",
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>",
                            },
                        ],
                    }
                ],
            }
        }

        schema = SurveySchema(relationships_question)

        assert "/question/answers/0/playback" in schema.pointers

    def test_summary_with_placeholder_extraction(self):
        summary_placeholder = {
            "summary": {
                "title": {
                    "text": "Answers for {person_name}",
                    "placeholders": [
                        {
                            "placeholder": "person_name",
                            "transforms": [
                                {
                                    "arguments": {
                                        "delimiter": " ",
                                        "list_to_concatenate": {
                                            "identifier": ["first-name", "last-name"],
                                            "source": "answers",
                                        },
                                    },
                                    "transform": "concatenate_list",
                                }
                            ],
                        }
                    ],
                },
                "item_title": {
                    "text": "{person_name}",
                    "placeholders": [
                        {
                            "placeholder": "person_name",
                            "transforms": [
                                {
                                    "arguments": {
                                        "delimiter": " ",
                                        "list_to_concatenate": {
                                            "identifier": ["first-name", "last-name"],
                                            "source": "answers",
                                        },
                                    },
                                    "transform": "concatenate_list",
                                }
                            ],
                        }
                    ],
                },
                "empty_list_text": "A list item",
                "add_link_text": "A list item",
            }
        }

        schema = SurveySchema(summary_placeholder)

        assert "/summary/item_title/text" in schema.pointers
        assert "/summary/title/text" in schema.pointers
        assert "/summary/empty_list_text" in schema.pointers
        assert "/summary/add_link_text" in schema.pointers

    def test_summary_without_placeholder_extraction(self):
        summary_placeholder = {
            "summary": {
                "title": "A title for the summary",
                "item_title": "A list item",
                "empty_list_text": "A list item",
                "add_link_text": "A list item",
            }
        }

        schema = SurveySchema(summary_placeholder)

        assert "/summary/title" in schema.pointers
        assert "/summary/item_title" in schema.pointers


class TestTranslate(unittest.TestCase):
    SCHEMA_WITH_SINGLE_PLACEHOLDER = {
        "id": "establishment-position-question",
        "title": {
            "placeholders": [
                {
                    "placeholder": "person_name_possessive",
                    "transforms": [
                        {
                            "arguments": {
                                "delimiter": " ",
                                "list_to_concatenate": {
                                    "identifier": ["first-name", "last-name"],
                                    "source": "answers",
                                },
                            },
                            "transform": "concatenate_list",
                        },
                        {
                            "arguments": {
                                "string_to_format": {"source": "previous_transform"}
                            },
                            "transform": "format_possessive",
                        },
                    ],
                }
            ],
            "text": "What is <em>{person_name_possessive}</em> position in this establishment?",
        },
        "type": "General",
    }

    SCHEMA_WITH_MULTIPLE_PLACEHOLDERS = {
        "question": {
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
                                "text": "{address}",
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
                                "text": "The address in {country}",
                            },
                            "value": "30-day-address",
                        },
                        {"label": "Another address", "value": "Another address",},
                    ],
                    "type": "Radio",
                }
            ],
            "id": "term-time-location-question",
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
                "text": "During term time, where does <em>{person_name}</em> usually live?",
            },
            "type": "General",
        }
    }

    def test_translate(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add(
            "Answering for this person",
            "WELSH - Answering for this person",
            auto_comments=["answer-id: feeling-answer"],
            context="Answer for: Who are you answering for??",
        )

        catalog.add(
            "Answering myself",
            "WELSH - Answering myself",
            auto_comments=["answer-id: feeling-answer"],
            context="Answer for: Who are you answering for??",
        )

        schema_translation.catalog = catalog

        schema = SurveySchema(
            {
                "sections": [
                    {
                        "question": {
                            "title": "Who are you answering for??",
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
                                        "content": [
                                            {
                                                "title": "Feeling answer",
                                                "description": "This should be answered to see if you are answering on behalf of someone else",
                                            }
                                        ],
                                    },
                                    "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                                }
                            ],
                        }
                    }
                ]
            }
        )
        translated = schema.translate(
            schema_translation, TestSurveySchema.LANGUAGE_CODE
        )

        expected = {
            "sections": [
                {
                    "question": {
                        "title": "Who are you answering for??",
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
                                    "content": [
                                        {
                                            "title": "Feeling answer",
                                            "description": "This should be answered to see if you are answering on behalf of someone else",
                                        }
                                    ],
                                },
                                "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                            }
                        ],
                    }
                }
            ]
        }

        assert expected == translated.schema

    def test_get_catalog(self):
        schema_data = {
            "sections": [
                {
                    "question": {
                        "title": "Please confirm the number of people who live at this household",
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
                                    "content": [
                                        {
                                            "title": "Feeling answer",
                                            "description": "This should be answered to see if you are answering on behalf of someone else",
                                        }
                                    ],
                                },
                                "instruction": "Tell respondent to turn to <strong>Showcard 1</strong>",
                            }
                        ],
                    }
                }
            ]
        }

        schema = SurveySchema(schema_data)
        catalog = schema.get_catalog

        actual_items = [message.id for message in catalog]

        assert schema_data["sections"][0]["question"]["title"] in actual_items
        assert (
            schema_data["sections"][0]["question"]["answers"][0]["label"]
            in actual_items
        )
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
            schema_data["sections"][0]["question"]["answers"][0]["guidance"]["content"][
                0
            ]["title"]
            in actual_items
        )
        assert (
            schema_data["sections"][0]["question"]["answers"][0]["guidance"]["content"][
                0
            ]["description"]
            in actual_items
        )
        assert (
            schema_data["sections"][0]["question"]["answers"][0]["instruction"]
            in actual_items
        )

        singluar_label = schema_data["sections"][0]["question"]["answers"][0][
            "options"
        ][0]["label"]["text_plural"]["forms"]["one"]
        plural_label = schema_data["sections"][0]["question"]["answers"][0]["options"][
            0
        ]["label"]["text_plural"]["forms"]["other"]

        assert (singluar_label, plural_label) in actual_items

    def test_get_catalog_uses_smart_quotes(self):
        schema_data = {
            "sections": [
                {"question": [{"title": "What is 'this persons' date of birth?"}]}
            ]
        }

        schema = SurveySchema(schema_data)

        catalog = schema.get_catalog

        actual_items = [message.id for message in catalog]

        assert "What is ‘this persons’ date of birth?" in actual_items

    def test_find_pointers_ignores_placeholders(self):
        schema = SurveySchema(self.SCHEMA_WITH_SINGLE_PLACEHOLDER)
        pointers = schema.get_title_pointers()

        assert "/title" not in pointers

    def test_get_placeholder_pointers(self):
        schema = SurveySchema(self.SCHEMA_WITH_MULTIPLE_PLACEHOLDERS)

        assert (
            "/question/answers/0/options/0/label/text"
            in schema.context_placeholder_pointers
        )
        assert (
            "/question/answers/0/options/1/label/text"
            in schema.context_placeholder_pointers
        )
        assert "/question/title/text" in schema.no_context_placeholder_pointers

    def test_placeholder_catalog_context(self):
        schema = SurveySchema(self.SCHEMA_WITH_MULTIPLE_PLACEHOLDERS)

        message = schema.get_catalog.get(
            "{address}",
            "Answer for: During term time, where does <em>{person_name}</em> usually live?",
        )
        assert message.auto_comments == ["answer-id: term-time-location-answer"]

    def test_get_text_plural_pointers(self):
        schema = SurveySchema(TestSurveySchema.PLURAL_FORMS_SCHEMA)

        assert (
            "/question/answers/0/options/0/label/text_plural"
            in schema.context_plural_pointers
        )

        assert "/question/title/text_plural" in schema.no_context_plural_pointers

    def test_placeholder_translation(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add(
            "What is <em>{person_name_possessive}</em> position in this establishment?",
            "WELSH - What is <em>{person_name_possessive}</em> position in this establishment?",
        )

        schema_translation.catalog = catalog

        schema = SurveySchema(self.SCHEMA_WITH_SINGLE_PLACEHOLDER)
        translated = schema.translate(
            schema_translation, TestSurveySchema.LANGUAGE_CODE
        )

        expected = {
            "id": "establishment-position-question",
            "title": {
                "placeholders": [
                    {
                        "placeholder": "person_name_possessive",
                        "transforms": [
                            {
                                "arguments": {
                                    "delimiter": " ",
                                    "list_to_concatenate": {
                                        "identifier": ["first-name", "last-name"],
                                        "source": "answers",
                                    },
                                },
                                "transform": "concatenate_list",
                            },
                            {
                                "arguments": {
                                    "string_to_format": {"source": "previous_transform"}
                                },
                                "transform": "format_possessive",
                            },
                        ],
                    }
                ],
                "text": "WELSH - What is <em>{person_name_possessive}</em> position in this establishment?",
            },
            "type": "General",
        }

        assert expected == translated.schema

    def test_variant_translation(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add(
            "First name",
            "WELSH - First name",
            auto_comments=["answer-id: first-name"],
            context="Answer for: What is your name?",
        )

        catalog.add(
            "First name",
            "WELSH - First name - Proxy",
            auto_comments=["answer-id: first-name"],
            context="Answer for: What is their name?",
        )

        schema_translation.catalog = catalog

        variant_schema = SurveySchema(TestSurveySchema.VARIANT_SCHEMA)

        translated = variant_schema.translate(
            schema_translation, TestSurveySchema.LANGUAGE_CODE
        )

        assert (
            translated.schema["question_variants"][0]["question"]["answers"][0]["label"]
            == "WELSH - First name"
        )
        assert (
            translated.schema["question_variants"][1]["question"]["answers"][0]["label"]
            == "WELSH - First name - Proxy"
        )

    def test_text_plural_translation(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

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
            auto_comments=["answer-id: confirm-count"],
            context="Answer for: {number_of_people} people live here, is this correct?",
        )

        schema_translation.catalog = catalog

        plural_forms_schema = SurveySchema(TestSurveySchema.PLURAL_FORMS_SCHEMA)

        translated = plural_forms_schema.translate(
            schema_translation, TestSurveySchema.LANGUAGE_CODE
        )

        forms_for_title = translated.schema["question"]["title"]["text_plural"]["forms"]

        assert forms_for_title["zero"] == "WELSH - zero"
        assert forms_for_title["one"] == "WELSH - one"
        assert forms_for_title["two"] == "WELSH - two"
        assert forms_for_title["few"] == "WELSH - few"
        assert forms_for_title["many"] == "WELSH - many"
        assert forms_for_title["other"] == "WELSH - other"

        forms_for_answer_label = translated.schema["question"]["answers"][0]["options"][
            0
        ]["label"]["text_plural"]["forms"]

        assert forms_for_answer_label["zero"] == "WELSH - zero"
        assert forms_for_answer_label["one"] == "WELSH - one"
        assert forms_for_answer_label["two"] == "WELSH - two"
        assert forms_for_answer_label["few"] == "WELSH - few"
        assert forms_for_answer_label["many"] == "WELSH - many"
        assert forms_for_answer_label["other"] == "WELSH - other"
