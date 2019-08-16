import unittest

from babel.messages import Catalog

from eq_translations.schema_translation import SchemaTranslation
from eq_translations.survey_schema import SurveySchema


class TestSurveySchema(unittest.TestCase):

    VARIANT_SCHEMA = {
        "id": "name",
        "question_variants": [{
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
                    }
                 },
                 {
                    "id": "last-name",
                    "label": "Last name",
                    "mandatory": False,
                    "type": "TextField"
                 }
              ],
              "id": "name-question",
              "title": "What is your name?",
              "type": "General"
           }
        }, {
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
                    }
                 },
                 {
                    "id": "last-name",
                    "label": "Last name",
                    "mandatory": False,
                    "type": "TextField"
                 }
              ],
              "id": "name-question",
              "title": "What is their name?",
              "type": "General"
           }
        }],
        "type": "Question"
    }

    def test_find_variant_pointers(self):
        schema = SurveySchema(TestSurveySchema.VARIANT_SCHEMA)

        pointers = schema.get_title_pointers()

        assert '/question_variants/0/question/title' in pointers
        assert '/question_variants/1/question/title' in pointers

    def test_get_messages(self):
        schema = SurveySchema()
        schema.load('./tests/schemas/test_translation.json')

        assert schema.pointers is not None

    def test_get_titles_messages(self):
        schema = SurveySchema({
            "sections": [{
                "type": "CalculatedSummary",
                "id": "block-3",
                "title": "Calculated Summary Main Title Block 2",
                "calculation": {
                    "calculation_type": "sum",
                    "answers_to_calculate": [
                        "first-number-answer",
                        "second-number-answer"
                    ],
                    "title": "Calculated Summary Calculation Title Block 2"
                }
            }]
        })
        pointers = schema.get_title_pointers()
        assert '/sections/0/title' in pointers
        assert '/sections/0/calculation/title' in pointers

        assert len(pointers) == 2

    def test_get_list_messages(self):
        schema = SurveySchema({
            "sections": [{
                "content": [{
                        "title": "Include:",
                        "list": [
                            "all employees in Great Britain (England, Scotland and Wales), both full and part-time, who received pay in the relevant period"
                        ]
                    },
                    {
                        "title": "Exclude:",
                        "list": [
                            "trainees on government schemes",
                            "employees working abroad unless paid directly from this business’s GB payroll",
                            "employees in Northern Ireland"
                        ]
                    }
                ]
            }]
        })

        pointers = schema.get_list_pointers()

        assert "/sections/0/content/0/list/0" in pointers
        assert "/sections/0/content/1/list/0" in pointers
        assert "/sections/0/content/1/list/1" in pointers
        assert "/sections/0/content/1/list/2" in pointers

        assert len(pointers) == 4

    def test_get_answer_messages(self):
        schema = SurveySchema({
            "sections": [{
                "question": [{
                    "answers": [{
                        "id": "confirm-feeling-answer",
                        "type": "Radio",
                        "label": "confirm",
                        "mandatory": True,
                        "options": [
                            {
                                "value": "Yes",
                                "label": "Yes"
                            },
                            {
                                "value": "No",
                                "label": "No"
                            }
                        ]
                    }]
                }]
            }]
        })

        pointers = schema.get_answer_pointers()

        assert '/sections/0/question/0/answers/0/options/0/label' in pointers
        assert '/sections/0/question/0/answers/0/options/1/label' in pointers

    def test_get_all_pointers(self):
        schema = SurveySchema({
            "sections": [{
                "content": [{
                        "title": "Include:",
                        "list": [
                            "all employees in Great Britain (England, Scotland and Wales), both full and part-time, who received pay in the relevant period"
                        ]
                    },
                    {
                        "title": "Exclude:",
                        "list": [
                            "trainees on government schemes",
                            "employees working abroad unless paid directly from this business’s GB payroll",
                            "employees in Northern Ireland"
                        ]
                    }
                ]
            }]
        })

        assert "/sections/0/content/0/title" in schema.pointers
        assert "/sections/0/content/1/title" in schema.pointers
        assert "/sections/0/content/0/list/0" in schema.pointers
        assert "/sections/0/content/1/list/0" in schema.pointers
        assert "/sections/0/content/1/list/1" in schema.pointers
        assert "/sections/0/content/1/list/2" in schema.pointers

        assert len(schema.pointers) == 6

    def test_get_parent_id(self):
        schema = SurveySchema({
            "sections": [{
                "question": {
                    "answers": [{
                        "id": "confirm-feeling-answer",
                        "type": "Radio",
                        "label": "confirm",
                        "mandatory": True,
                        "options": [
                            {
                                "value": "Yes",
                                "label": "Yes"
                            },
                            {
                                "value": "No",
                                "label": "No"
                            }
                        ]
                    }]
                }
            }]
        })

        option_parent_id = schema.get_parent_id('/sections/0/question/answers/0/options/0/label')
        answer_parent_id = schema.get_parent_id('/sections/0/question/answers/0/label')

        assert option_parent_id == 'confirm-feeling-answer'
        assert answer_parent_id == 'confirm-feeling-answer'

    def test_get_parent_question_pointer(self):

        schema = SurveySchema()
        parent_question_pointer = schema.get_parent_question_pointer('/question/0/answers/0/options/0/label')

        assert parent_question_pointer == '/question'

    def test_get_parent_question(self):
        original_question = {
            "question": {
                "answers": [{
                    "id": "confirm-feeling-answer",
                    "type": "Radio",
                    "label": "confirm",
                    "mandatory": True,
                    "options": [
                        {
                            "value": "Yes",
                            "label": "Yes"
                        },
                        {
                            "value": "No",
                            "label": "No"
                        }
                    ]
                }],
            },
            "title": "text",
        }

        schema = SurveySchema({
            "question": original_question
        })
        parent_question = schema.get_parent_question('/question/0/answers/0/options/0/label')
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
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>"
                            },
                            {
                                "label": "Legally registered civil partner",
                                "value": "Legally registered civil partner",
                                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>",
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>"
                            },
                            {
                                "label": "Son or daughter",
                                "value": "Son or daughter",
                                "title": "Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>",
                                "playback": "{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>"
                            }
                        ]
                    }
                ]
            }
        }

        schema = SurveySchema(relationships_question)

        assert "/question/answers/0/playback" in schema.pointers


    def test_summary_item_title_with_placeholder_extraction(self):
        summary_placeholder = {
            "summary": {
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
                                            "source": "answers"
                                        }
                                    },
                                    "transform": "concatenate_list"
                                }
                            ]
                        }
                    ]
                }
            }
        }

        schema = SurveySchema(summary_placeholder)
        assert "/summary/item_title/text" in schema.pointers

    def test_summary_item_title_without_placeholder_extraction(self):
        summary_placeholder = {
            "summary": {
                "item_title": "A list item"
            }
        }

        schema = SurveySchema(summary_placeholder)
        assert "/summary/item_title" in schema.pointers


class TestTranslate(unittest.TestCase):

    def test_translate(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add("Answering for this person",
                    "WELSH - Answering for this person",
                    auto_comments=["answer-id: feeling-answer"],
                    context="Answer for: Who are you answering for??")

        catalog.add("Answering myself",
                    "WELSH - Answering myself",
                    auto_comments=["answer-id: feeling-answer"],
                    context="Answer for: Who are you answering for??")

        schema_translation.catalog = catalog

        schema = SurveySchema({
            "sections": [{
                "question": {
                    "title": "Who are you answering for??",
                    "answers": [{
                        "type": "Radio",
                        "id": "feeling-answer",
                        "label": "Feeling answer",
                        "mandatory": True,
                        "options": [{
                                "label": "Answering for this person",
                                "value": "good"
                            },
                            {
                                "label": "Answering myself",
                                "value": "bad",
                                "detail_answer": {
                                    "id": "feeling-bad-answer",
                                    "label": "Specify why answering for yourself is bad",
                                    "mandatory": True,
                                    "type": "TextField"
                                }
                            }
                        ],
                        "guidance": {
                            "hide_guidance": "Hide feeling answer help",
                            "show_guidance": "Show feeling answer help",
                            "content": [{
                                "title": "Feeling answer",
                                "description": "This should be answered to see if you are answering on behalf of someone else"
                            }]
                        }
                    }]
                }
            }]
        })
        translated = schema.translate(schema_translation)

        expected = {
            "sections": [{
                "question": {
                    "title": "Who are you answering for??",
                    "answers": [{
                        "type": "Radio",
                        "id": "feeling-answer",
                        "label": "Feeling answer",
                        "mandatory": True,
                        "options": [{
                                "label": "WELSH - Answering for this person",
                                "value": "good"
                            },
                            {
                                "label": "WELSH - Answering myself",
                                "value": "bad",
                                "detail_answer": {
                                    "id": "feeling-bad-answer",
                                    "label": "Specify why answering for yourself is bad",
                                    "mandatory": True,
                                    "type": "TextField"
                                }
                            }
                        ],
                        "guidance": {
                            "hide_guidance": "Hide feeling answer help",
                            "show_guidance": "Show feeling answer help",
                            "content": [{
                                "title": "Feeling answer",
                                "description": "This should be answered to see if you are answering on behalf of someone else"
                            }]
                        }
                    }]
                }
            }]
        }

        assert expected == translated.schema

    def test_get_catalog(self):
        schema_data = {
            "sections": [{
                "question": {
                    "title": "Who are you answering for??",
                    "answers": [{
                        "type": "Radio",
                        "id": "feeling-answer",
                        "label": "Feeling answer",
                        "mandatory": True,
                        "options": [{
                                "label": "Answering for this person",
                                "value": "good"
                            },
                            {
                                "label": "Answering myself",
                                "value": "bad",
                                "detail_answer": {
                                "id": "feeling-bad-answer",
                                "label": "Specify why answering for yourself is bad",
                                "mandatory": True,
                                "type": "TextField"
                                }
                            }
                        ],
                        "guidance": {
                            "hide_guidance": "Hide feeling answer help",
                            "show_guidance": "Show feeling answer help",
                            "content": [{
                                "title": "Feeling answer",
                                "description": "This should be answered to see if you are answering on behalf of someone else"
                            }]
                        }
                    }]
                }
            }]
        }

        schema = SurveySchema(schema_data)
        catalog = schema.get_catalog()

        actual_items = [message.id for message in catalog]
        assert schema_data['sections'][0]['question']['title'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['label'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['options'][0]['label'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['options'][1]['label'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['options'][1]['detail_answer']['label'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['guidance']['hide_guidance'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['guidance']['show_guidance'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['guidance']['content'][0]['title'] in actual_items
        assert schema_data['sections'][0]['question']['answers'][0]['guidance']['content'][0]['description'] in actual_items

    def test_get_catalog_uses_smart_quotes(self):
        schema_data = {
            "sections": [{
                "question": [{
                    "title": "What is 'this persons' date of birth?"
                }]
            }]
        }

        schema = SurveySchema(schema_data)

        catalog = schema.get_catalog()

        actual_items = [message.id for message in catalog]

        assert "What is ‘this persons’ date of birth?" in actual_items

    def test_find_pointers_ignores_placeholders(self):
        schema = SurveySchema({
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
                                        "identifier": [
                                            "first-name",
                                            "last-name"
                                        ],
                                        "source": "answers"
                                    }
                                },
                                "transform": "concatenate_list"
                            },
                            {
                                "arguments": {
                                    "string_to_format": {
                                        "source": "previous_transform"
                                    }
                                },
                                "transform": "format_possessive"
                            }
                        ]
                    }
                ],
                "text": "What is <em>{person_name_possessive}</em> position in this establishment?"
            },
            "type": "General"
        })
        pointers = schema.get_title_pointers()

        assert '/title' not in pointers

    def test_get_placeholder_pointers(self):
        schema = SurveySchema({
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
                                      "source": "metadata"
                                   }
                                }
                             ],
                             "text": "{address}"
                          },
                          "value": "household-address"
                       },
                       {
                          "label": {
                             "placeholders": [
                                {
                                   "placeholder": "country",
                                   "value": {
                                      "identifier": "another-address-answer-other-country",
                                      "source": "answers"
                                   }
                                }
                             ],
                             "text": "The address in {country}"
                          },
                          "value": "30-day-address"
                       },
                       {
                          "label": "Another address",
                          "value": "Another address"
                       }
                    ],
                    "type": "Radio"
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
                                   "identifier": [
                                      "first-name",
                                      "last-name"
                                   ],
                                   "source": "answers"
                                }
                             },
                             "transform": "concatenate_list"
                          }
                       ]
                    }
                 ],
                 "text": "During term time, where does <em>{person_name}</em> usually live?"
              },
              "type": "General"
            }
        })

        assert '/question/answers/0/options/0/label/text' in schema.context_placeholder_pointers
        assert '/question/answers/0/options/1/label/text' in schema.context_placeholder_pointers
        assert '/question/title/text' in schema.no_context_placeholder_pointers

    def test_placeholder_catalog_context(self):
        schema = SurveySchema({
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
                                      "source": "metadata"
                                   }
                                }
                             ],
                             "text": "{address}"
                          },
                          "value": "household-address"
                       },
                       {
                          "label": "Another address",
                          "value": "Another address"
                       }
                    ],
                    "type": "Radio"
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
                                   "identifier": [
                                      "first-name",
                                      "last-name"
                                   ],
                                   "source": "answers"
                                }
                             },
                             "transform": "concatenate_list"
                          }
                       ]
                    }
                 ],
                 "text": "During term time, where does <em>{person_name}</em> usually live?"
              },
              "type": "General"
            }
        })

        message = schema.get_catalog().get(
            '{address}', 'Answer for: During term time, where does <em>{person_name}</em> usually live?'
        )
        assert message.auto_comments == ['answer-id: term-time-location-answer']

    def test_placeholder_translation(self):

        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add("What is <em>{person_name_possessive}</em> position in this establishment?",
                    "WELSH - What is <em>{person_name_possessive}</em> position in this establishment?")

        schema_translation.catalog = catalog

        schema = SurveySchema({
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
                                        "identifier": [
                                            "first-name",
                                            "last-name"
                                        ],
                                        "source": "answers"
                                    }
                                },
                                "transform": "concatenate_list"
                            },
                            {
                                "arguments": {
                                    "string_to_format": {
                                        "source": "previous_transform"
                                    }
                                },
                                "transform": "format_possessive"
                            }
                        ]
                    }
                ],
                "text": "What is <em>{person_name_possessive}</em> position in this establishment?"
            },
            "type": "General"
        })
        translated = schema.translate(schema_translation)

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
                                        "identifier": [
                                            "first-name",
                                            "last-name"
                                        ],
                                        "source": "answers"
                                    }
                                },
                                "transform": "concatenate_list"
                            },
                            {
                                "arguments": {
                                    "string_to_format": {
                                        "source": "previous_transform"
                                    }
                                },
                                "transform": "format_possessive"
                            }
                        ]
                    }
                ],
                "text": "WELSH - What is <em>{person_name_possessive}</em> position in this establishment?"
            },
            "type": "General"
        }

        assert expected == translated.schema

    def test_variant_translation(self):
        schema_translation = SchemaTranslation()

        catalog = Catalog()

        catalog.add("First name",
                    "WELSH - First name",
                    auto_comments=["answer-id: first-name"],
                    context="Answer for: What is your name?")

        catalog.add("First name",
                    "WELSH - First name - Proxy",
                    auto_comments=["answer-id: first-name"],
                    context="Answer for: What is their name?")

        schema_translation.catalog = catalog

        variant_schema = SurveySchema(TestSurveySchema.VARIANT_SCHEMA)

        translated = variant_schema.translate(schema_translation)

        assert translated.schema['question_variants'][0]['question']['answers'][0]['label'] == "WELSH - First name"
        assert translated.schema['question_variants'][1]['question']['answers'][0]['label'] == "WELSH - First name - Proxy"
