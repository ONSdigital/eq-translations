from eq_translations.survey_schema import SurveySchema
from eq_translations.translatable_item import TranslatableItem


def test_question_variants(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question_variants/0/question/title",
            description="Question text",
            value="What is your name?",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/question_variants/1/question/title",
            description="Question text",
            value="What is their name?",
        )
        in translatable_items
    )


def test_content_variants(schema_with_content_variants):
    schema = SurveySchema(schema_with_content_variants)

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/title",
            description="Content page main heading",
            value="Main job",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content_variants/1/content/title",
            description="Content page main heading",
            value="Last main job",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content_variants/0/content/contents/0/description",
            description="Content page description",
            value="We will now ask you questions about your main job",
            context="Main job",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content_variants/1/content/contents/0/description",
            description="Content page description",
            value="We will now ask you questions about your last main job",
            context="Last main job",
        )
        in translatable_items
    )


def test_validation_messages(schema_with_question_variants):
    schema = SurveySchema(schema_with_question_variants)
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question_variants/0/question/answers/0/validation/messages/MANDATORY_TEXTFIELD",
            description="Answer error message",
            value="Please enter a name or remove the person to continue",
            context="What is your name?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question_variants/1/question/answers/0/validation/messages/MANDATORY_TEXTFIELD",
            description="Answer error message",
            value="Please enter a name or remove the person to continue",
            context="What is their name?",
        )
        in translatable_items
    )


def test_titles():
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
            description="Question text",
            value="We calculate the total of currency values entered to be %(total)s. Is this correct?",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/question/calculation/title",
            description="Question calculation title",
            value="Grand total of previous values",
            context="We calculate the total of currency values entered to be %(total)s. Is this correct?",
        )
        in translatable_items
    )

    assert len(translatable_items) == 2


def test_string_objects_in_list():
    schema = SurveySchema(
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
            "id": "main-employment-block",
            "type": "Interstitial",
        }
    )

    translatable_items = list(schema.translatable_items)
    pointers = [item.pointer for item in translatable_items]

    assert (
        TranslatableItem(
            pointer="/content/contents/0/list/0",
            description="Content page list item",
            value="all part-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
            context="Main job",
        )
        in translatable_items
    )

    # Placeholder 'text' is extracted explicitly
    assert "/content/contents/0/list/1" not in pointers

    assert (
        TranslatableItem(
            pointer="/content/contents/0/list/1/text",
            description="Content page list item",
            value="all trainees on government schemes on {date}",
            context="Main job",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content/contents/0/list/2",
            description="Content page list item",
            value="all full-time employees in Great Britain (England, Scotland and Wales) who received pay in the relevant period",
            context="Main job",
        )
        in translatable_items
    )

    # Plural form 'text_plural' is extracted explicitly
    assert "/content/contents/0/list/3" not in pointers

    assert (
        TranslatableItem(
            pointer="/content/contents/0/list/3/text_plural/forms",
            description="Content page list item",
            value={
                "one": "the person who lives here",
                "other": "the people who live here",
            },
            context="Main job",
        )
        in translatable_items
    )


def test_when_rule_list_property_not_extracted():
    schema = SurveySchema(
        {
            "content": {
                "contents": [{"list": ["trainees on government schemes",],}],
                "title": "Content title",
            },
            "when": [{"condition": "greater than", "list": "household", "value": 5}],
        }
    )

    translatable_items = list(schema.translatable_items)
    pointers = [item.pointer for item in translatable_items]
    assert {"pointer": "/when/list"} not in pointers


def test_get_text_plural_pointers(schema_with_plurals):
    schema = SurveySchema(schema_with_plurals)
    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/label/text_plural/forms",
            description="Answer option",
            value={
                "one": "Yes, {number_of_people} person lives here",
                "other": "Yes, {number_of_people} people live here",
            },
            context="{number_of_people} people live here, is this correct?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/title/text_plural/forms",
            description="Question text",
            value={
                "one": "{number_of_people} person lives here, is this correct?",
                "other": "{number_of_people} people live here, is this correct?",
            },
        )
        in translatable_items
    )


def test_answer_additional_context():
    schema = SurveySchema(
        {
            "question": {
                "type": "General",
                "id": "question",
                "title": "How are you feeling?",
                "answers": [
                    {
                        "id": "feeling-answer",
                        "type": "Texfield",
                        "label": "Feeling",
                        "description": "Describe how you're feeling",
                        "mandatory": True,
                    }
                ],
            }
        }
    )

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/description",
            description="Answer description",
            value="Describe how you're feeling",
            context="How are you feeling?",
            additional_context=["For answer: Feeling"],
        )
        in translatable_items
    )


def test_answer_option_additional_context():
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
                            {
                                "value": "Yes",
                                "label": "Yes",
                                "description": "Select this if you're happy",
                            },
                            {
                                "value": "No",
                                "label": "No",
                                "description": "Select this if you're not happy",
                            },
                        ],
                    }
                ],
            }
        }
    )

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/description",
            description="Answer option description",
            value="Select this if you're happy",
            context="Are you happy?",
            additional_context=["For answer option: Yes"],
        )
        in translatable_items
    )


def test_content_list_additional_context():
    schema = SurveySchema(
        {
            "content": {
                "contents": [
                    {"list": ["list with no title"]},
                    {"title": "list title", "list": ["list with title"]},
                    {
                        "description": "list description",
                        "list": ["list with description"],
                    },
                    {
                        "title": "list title",
                        "description": "list description",
                        "list": ["list with title and description"],
                    },
                ],
                "title": "Content title",
            }
        }
    )

    translatable_items = list(schema.translatable_items)

    assert (
        TranslatableItem(
            pointer="/content/contents/0/list/0",
            description="Content page list item",
            value="list with no title",
            context="Content title",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content/contents/1/list/0",
            description="Content page list item",
            value="list with title",
            context="Content title",
            additional_context=["For heading: list title"],
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content/contents/2/list/0",
            description="Content page list item",
            value="list with description",
            context="Content title",
            additional_context=["For description: list description"],
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/content/contents/3/list/0",
            description="Content page list item",
            value="list with title and description",
            context="Content title",
            additional_context=[
                "For heading: list title",
                "For description: list description",
            ],
        )
        in translatable_items
    )


def test_answer_label():
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
            description="Answer option",
            value="Yes",
            context="Are you happy?",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/1/label",
            description="Answer option",
            value="No",
            context="Are you happy?",
        )
        in translatable_items
    )


def test_relationship_playback():
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
            description="Relationships playback template",
            value="{second_person_name} is {first_person_name_possessive} <em>…</em>",
            context="Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/0/playback",
            description="Relationships answer option playback text",
            value="{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>",
            context="Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/1/playback",
            description="Relationships answer option playback text",
            value="{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>",
            context="Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
        )
        in translatable_items
    )

    assert (
        TranslatableItem(
            pointer="/question/answers/0/options/2/playback",
            description="Relationships answer option playback text",
            value="{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>",
            context="Thinking of {first_person_name}, {second_person_name} is their <em>...</em>",
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
        TranslatableItem(
            pointer="/summary/item_title/text",
            description="List collector summary item",
            value="{person_name}",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/add_link_text",
            description="List collector add link text",
            value="A list item",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/empty_list_text",
            description="List collector empty list text",
            value="A list item",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/title/text",
            description="List collector summary heading",
            value="Answers for {person_name}",
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
        TranslatableItem(
            pointer="/summary/title",
            description="List collector summary heading",
            value="A title for the summary",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/item_title",
            description="List collector summary item",
            value="A list item",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/empty_list_text",
            description="List collector empty list text",
            value="An empty title text",
        )
        in translatable_items
    )
    assert (
        TranslatableItem(
            pointer="/summary/add_link_text",
            description="List collector add link text",
            value="An add link text",
        )
        in translatable_items
    )


def test_get_schema_language():
    survey_schema = SurveySchema()
    survey_schema.load("tests/schemas/en/test_translation.json")

    assert survey_schema.language == "en"


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
