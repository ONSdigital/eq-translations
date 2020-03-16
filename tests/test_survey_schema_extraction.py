from eq_translations.survey_schema import SurveySchema
from eq_translations.translatable_item import TranslatableItem


def test_variant_translatable_items(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question_variants/0/question/title", value="What is your name?"
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/question_variants/1/question/title", value="What is their name?"
        )
        in translatable_items
    )


def test_validation_messages_translatable_items(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question_variants/0/question/answers/0/validation/messages/MANDATORY_TEXTFIELD",
            value="Please enter a name or remove the person to continue",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question_variants/1/question/answers/0/validation/messages/MANDATORY_TEXTFIELD",
            value="Please enter a name or remove the person to continue",
        )
        in translatable_items
    )


def test_titles_translatable_items():
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
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/title",
            value="We calculate the total of currency values entered to be %(total)s. Is this correct?",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/question/calculation/title",
            value="Grand total of previous values",
        )
        in translatable_items
    )

    assert len(translatable_items) == 2


def test_list_translatable_items():
    schema = SurveySchema(
        {
            "content_variants": [
                {
                    "content": {
                        "contents": [
                            {
                                "list": [
                                    "all part-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
                                    {
                                        "placeholders": [
                                            {
                                                "placeholder": "date",
                                                "transforms": [
                                                    {
                                                        "arguments": {
                                                            "date_format": "d MMMM yyyy",
                                                            "date_to_format": {
                                                                "value": "2019-10-09"
                                                            },
                                                        },
                                                        "transform": "format_date",
                                                    }
                                                ],
                                            }
                                        ],
                                        "text": "all trainees on government schemes on {date}",
                                    },
                                    "all full-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
                                    {
                                        "text_plural": {
                                            "forms": {
                                                "one": "the person who lives here",
                                                "other": "the people who live here",
                                            },
                                            "count": {
                                                "source": "answers",
                                                "identifier": "number-of-people-answer",
                                            },
                                        }
                                    },
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

    translatable_items = list(schema.translatable_items)
    pointers = [item.pointer for item in translatable_items]

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/contents/0/list/0",
            value="all part-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
        )
        in translatable_items
    )

    # Placeholder 'text' is extracted explicitly
    assert "/content_variants/0/content/contents/0/list/1" not in pointers

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/contents/0/list/text",
            value="all trainees on government schemes on {date}",
            context=None,
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/contents/0/list/2",
            value="all full-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
        )
        in translatable_items
    )

    # Plural form 'text_plural' is extracted explicitly
    assert "/content_variants/0/content/contents/0/list/3" not in pointers

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/contents/0/list/text_plural/forms",
            value={
                "one": "the person who lives here",
                "other": "the people who live here",
            },
            context=None,
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content_variants/1/content/contents/0/list/0",
            value="trainees on government schemes",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/content_variants/1/content/contents/0/list/1",
            value="employees working abroad unless paid directly from this business’s GB payroll",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/content_variants/1/content/contents/0/list/2",
            value="employees in Northern Ireland",
        )
        in translatable_items
    )

    assert {"pointer": "/content_variants/0/when/list"} not in translatable_items
    assert {"pointer": "/content_variants/1/when/list"} not in translatable_items


def test_answer_label_translatable_items():
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

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/label",
            value="Yes",
            context="Answer for: Are you happy?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/1/label",
            value="No",
            context="Answer for: Are you happy?",
        )
        in translatable_items
    )


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


def test_relationship_playback_translatable_items():
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
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/playback",
            value="{second_person_name} is {first_person_name_possessive} <em>…</em>",
            context="Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/playback",
            value="{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>",
            context="Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/1/playback",
            value="{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>",
            context="Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/2/playback",
            value="{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>",
            context="Answer for: Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )


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
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(pointer="/summary/item_title/text", value="{person_name}")
        in translatable_items
    )
    assert (
        TranslatableItem(pointer="/summary/add_link_text", value="A list item")
        in translatable_items
    )
    assert (
        TranslatableItem(pointer="/summary/empty_list_text", value="A list item")
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/title/text", value="Answers for {person_name}"
        )
        in translatable_items
    )


def test_summary_without_placeholder_extraction():
    summary_placeholder = {
        "summary": {
            "title": "A title for the summary",
            "item_title": "A list item",
            "empty_list_text": "An empty title text",
            "add_link_text": "An add link text",
        }
    }

    schema = SurveySchema(summary_placeholder)
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(pointer="/summary/title", value="A title for the summary")
        in translatable_items
    )
    assert (
        TranslatableItem(pointer="/summary/item_title", value="A list item")
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/empty_list_text", value="An empty title text"
        )
        in translatable_items
    )
    assert (
        TranslatableItem(pointer="/summary/add_link_text", value="An add link text")
        in translatable_items
    )


def test_all_pointers_resolve_to_correct_instance():
    survey_schema = SurveySchema()
    survey_schema.load("tests/schemas/en/test_translation.json")

    for translatable_item in survey_schema.translatable_items:
        if not translatable_item.value:
            continue

        if "/text_plural" in translatable_item.pointer:
            assert isinstance(translatable_item.value, dict)
        else:
            assert isinstance(translatable_item.value, str)
