from eq_translations.survey_schema import SurveySchema


def test_variant_pointers(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)

    pointers = schema.pointer_dicts

    assert {"pointer": "/question_variants/0/question/title"} in pointers
    assert {"pointer": "/question_variants/1/question/title"} in pointers


def test_messages_pointers(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)
    pointers = schema.pointer_dicts

    assert {
        "pointer": "/question_variants/0/question/answers/0/validation/messages/MANDATORY_TEXTFIELD"
    } in pointers

    assert {
        "pointer": "/question_variants/1/question/answers/0/validation/messages/MANDATORY_TEXTFIELD"
    } in pointers


def test_titles_pointers():
    schema = SurveySchema(
        {
            "question": {
                "type": "CalculatedSummary",
                "id": "currency-total-playback-skipped-fourth",
                "title": "We calculate the total of currency values entered to be %(total)s. Is this correct?",
                "calculation": {
                    "calculation_type": "sum",
                    "answers_to_calculate": [
                        "first-number-answer",
                        "second-number-answer",
                        "second-number-answer-also-in-total",
                        "third-number-answer",
                    ],
                    "title": "Grand total of previous values",
                },
            }
        }
    )
    pointers = schema.pointer_dicts

    assert {"pointer": "/question/title"} in pointers
    assert {"pointer": "/question/calculation/title"} in pointers

    assert len(pointers) == 2


def test_list_pointers():
    schema = SurveySchema(
        {
            "content_variants": [
                {
                    "content": {
                        "contents": [
                            {
                                "list": [
                                    "all employees in Great Britain (England, Scotland and Wales), "
                                    "both full and part-time, who received pay in the relevant period"
                                ]
                            }
                        ],
                        "title": "Main job",
                    },
                    "when": [{"condition": "equals", "list": "household", "value": 0}],
                },
                {
                    "content": {
                        "contents": [
                            {
                                "title": "Exclude:",
                                "list": [
                                    "trainees on government schemes",
                                    "employees working abroad unless paid directly from this business’s GB payroll",
                                    "employees in Northern Ireland",
                                ],
                            }
                        ],
                        "title": "Last main job",
                    },
                    "when": [
                        {"condition": "greater than", "list": "household", "value": 5}
                    ],
                },
            ],
            "id": "main-employment-block",
            "type": "Interstitial",
        }
    )

    pointers = schema.pointer_dicts

    assert {"pointer": "/content_variants/0/content/contents/0/list/0"} in pointers
    assert {"pointer": "/content_variants/1/content/contents/0/list/0"} in pointers
    assert {"pointer": "/content_variants/1/content/contents/0/list/1"} in pointers
    assert {"pointer": "/content_variants/1/content/contents/0/list/2"} in pointers

    assert {"pointer": "/content_variants/0/when/list"} not in pointers
    assert {"pointer": "/content_variants/1/when/list"} not in pointers


def test_answer_label_pointers():
    schema = SurveySchema(
        {
            "question": {
                "type": "General",
                "id": "question-2",
                "title": "Are you happy?",
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
                ],
            }
        }
    )

    pointers = schema.pointer_dicts

    assert {
        "pointer": "/question/answers/0/options/0/label",
        "context": "Answer for: Are you happy?",
    } in pointers

    assert {
        "pointer": "/question/answers/0/options/1/label",
        "context": "Answer for: Are you happy?",
    } in pointers


def test_get_parent_question():
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


def test_relationship_playback_pointers():
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

    assert {
        "pointer": "/question/answers/0/playback",
        "context": "Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
    } in schema.pointer_dicts

    assert {
        "pointer": "/question/answers/0/options/0/playback",
        "context": "Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
    } in schema.pointer_dicts

    assert {
        "pointer": "/question/answers/0/options/1/playback",
        "context": "Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
    } in schema.pointer_dicts

    assert {
        "pointer": "/question/answers/0/options/2/playback",
        "context": "Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
    } in schema.pointer_dicts


def test_summary_with_placeholder_extraction():
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
    pointers = schema.pointer_dicts

    assert {"pointer": "/summary/item_title/text"} in pointers
    assert {"pointer": "/summary/add_link_text"} in pointers
    assert {"pointer": "/summary/empty_list_text"} in pointers
    assert {"pointer": "/summary/title/text"} in pointers


def test_summary_without_placeholder_extraction():
    summary_placeholder = {
        "summary": {
            "title": "A title for the summary",
            "item_title": "A list item",
            "empty_list_text": "A list item",
            "add_link_text": "A list item",
        }
    }

    schema = SurveySchema(summary_placeholder)
    pointers = schema.pointer_dicts

    assert {"pointer": "/summary/title"} in pointers
    assert {"pointer": "/summary/item_title"} in pointers
    assert {"pointer": "/summary/empty_list_text"} in pointers
    assert {"pointer": "/summary/add_link_text"} in pointers
