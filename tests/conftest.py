import pytest


@pytest.fixture
def schema_with_question_variants():
    return {
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


@pytest.fixture
def schema_with_content_variants():
    return {
        "content_variants": [
            {
                "content": {
                    "contents": [
                        {
                            "description": "We will now ask you questions about your main job",
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
                            "description": "We will now ask you questions about your last main job",
                        }
                    ],
                    "title": "Last main job",
                },
                "when": [
                    {"condition": "greater than", "list": "household", "value": 0}
                ],
            },
        ],
        "id": "main-job",
        "type": "Interstitial",
    }


@pytest.fixture
def schema_with_plurals():
    return {
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


@pytest.fixture
def schema_with_placeholders():
    return {
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
                                        "identifier": [
                                            "first-name",
                                            "last-name",
                                        ],
                                        "source": "answers",
                                    },
                                },
                                "transform": "concatenate_list",
                            }
                        ],
                    }
                ],
                "text": "During term time, where does <strong>{person_name}</strong> usually live?",
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
                    ],
                    "type": "Radio",
                }
            ],
        }
    }
