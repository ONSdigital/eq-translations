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


def test_compare_target_schema_missing_pointer():

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


def test_compare_target_schema_no_missing_pointer():

    source_schema = {"a": {"test": [{"item": {}}, {"item": {}}]}}

    target_schema = {"a": {"test": [{"item": {}}, {"item": {}}]}}

    differences = compare_schemas(source_schema, target_schema)

    assert not differences


def test_validate_missing_translated_plural_forms():
    translated_schema = {
        "text_plural": {
            "forms": {"one": "one", "other": "other", "many": "many", "few": ""},
            "count": {"source": "answers", "identifier": "number-of-people-answer"},
        }
    }

    missing_plural_forms = validate_translated_plural_forms(translated_schema, "cy")
    plurals = [missing_plural[1] for missing_plural in missing_plural_forms]

    assert "one" not in plurals
    assert "other" not in plurals
    assert "many" not in plurals

    assert "few" in plurals
    assert "zero" in plurals
    assert "two" in plurals

    assert len(missing_plural_forms) == 3


def test_validate_no_missing_translated_plural_forms():
    translated_schema = {
        "text_plural": {
            "forms": {"one": "one", "other": "other"},
            "count": {"source": "answers", "identifier": "number-of-people-answer"},
        }
    }

    missing_plural_forms = validate_translated_plural_forms(translated_schema, "en")

    assert not missing_plural_forms
