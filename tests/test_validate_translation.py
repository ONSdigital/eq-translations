from eq_translations.utils import get_plural_forms_for_language
from eq_translations.validate_translation import (
    compare_schemas,
    validate_translated_plural_forms,
)


def test_compare_source_schema():
    source_schema = {
        "this": "is",
        "a": {
            "test": [
                {"item": {}},
                {"item": {}},
                {"item": {}},
                {"item": {}},
                {"item": {}},
            ]
        },
    }

    target_schema = {"this": "is", "a": {"test": [{"item": {}}, {"item": {}}]}}

    differences = compare_schemas(source_schema, target_schema)

    assert "/a/test/2" in differences
    assert "/a/test/3" in differences
    assert "/a/test/4" in differences
    assert "/a/test/2/item" in differences
    assert "/a/test/3/item" in differences
    assert "/a/test/4/item" in differences

    assert len(differences) == 6


def test_compare_target_schema():

    source_schema = {"a": {"test": [{"item": {}}, {"item": {}}]}}

    target_schema = {
        "this": "is",
        "a": {
            "test": [{"item": {}}, {"item": {}}, {"item": {}}],
            "key": [{"x": {"2": 3}}, "y", "z"],
        },
    }

    differences = compare_schemas(source_schema, target_schema)

    assert "/this" in differences
    assert "/a/test/2" in differences
    assert "/a/test/2/item" in differences
    assert "/a/key" in differences
    assert "/a/key/0" in differences
    assert "/a/key/0/x" in differences
    assert "/a/key/0/x/2" in differences
    assert "/a/key/1" in differences
    assert "/a/key/2" in differences

    assert len(differences) == 9


def test_validate_translated_plural_forms():
    translated_schema = {
        "text_plural": {
            "forms": {"one": "one", "other": "other", "many": "many", "few": ""},
            "count": {"source": "answers", "identifier": "number-of-people-answer"},
        },
        "placeholders": [
            {
                "placeholder": "number_of_people",
                "value": {"source": "answers", "identifier": "number-of-people-answer"},
            }
        ],
    }

    plural_forms = get_plural_forms_for_language("cy")
    missing_plural_forms = validate_translated_plural_forms(
        translated_schema, plural_forms
    )

    assert "one" not in missing_plural_forms
    assert "other" not in missing_plural_forms
    assert "many" not in missing_plural_forms

    assert "few" in missing_plural_forms
    assert "zero" in missing_plural_forms
    assert "two" in missing_plural_forms

    assert len(missing_plural_forms) == 3
