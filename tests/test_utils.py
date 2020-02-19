from eq_translations.utils import (
    get_parent_pointer,
    find_pointers_containing,
    find_pointers_to,
    list_pointers,
    are_dumb_strings_equal,
)


def test_find_pointers_containing_root():
    schema = {"test": ""}

    pointers = [p for p in find_pointers_containing(schema, "test")]

    assert pointers == []


def test_find_pointers_containing_element():
    schema = {"this": "is", "a": {"test": "schema"}}

    pointers = find_pointers_containing(schema, "test")

    assert "/a" in pointers


def test_find_pointers_containing_list():
    schema = {
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

    pointers = find_pointers_containing(schema, "item")

    assert "/a/test/0" in pointers
    assert "/a/test/1" in pointers
    assert "/a/test/2" in pointers
    assert "/a/test/3" in pointers
    assert "/a/test/4" in pointers


def test_find_pointers_to_root():
    schema = {"test": {}, "foo": {}, "bar": {}}

    pointers = find_pointers_to(schema, "test")

    assert "/test" in pointers


def test_find_pointers_to_element():
    schema = {"this": "is", "a": {"test": "schema"}}

    pointers = find_pointers_to(schema, "test")

    assert "/a/test" in pointers


def test_find_pointers_to_list():
    schema = {
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

    pointers = find_pointers_to(schema, "item")

    assert "/a/test/0/item" in pointers
    assert "/a/test/1/item" in pointers
    assert "/a/test/2/item" in pointers
    assert "/a/test/3/item" in pointers
    assert "/a/test/4/item" in pointers


def test_get_parent_pointer():
    option_parent_pointer = get_parent_pointer("/questions/0/answers/0/options/0/label")
    answer_parent_pointer = get_parent_pointer("/questions/0/answers/0/label")

    assert option_parent_pointer == "/questions/0/answers/0/options/0"
    assert answer_parent_pointer == "/questions/0/answers/0"


def test_list_pointers():
    schema = {
        "this": "is",
        "a": {
            "test": [
                {"item": {}},
                {"item": {}},
                {"item": {}},
                {"item": {}},
                {"item": {}},
            ],
            "key": [{"x": {"2": 3}}, "y", "z"],
        },
    }

    pointers = list(list_pointers(schema))

    assert "/a" in pointers
    assert "/this" in pointers
    assert "/a/test" in pointers
    assert "/a/test/0" in pointers
    assert "/a/test/1" in pointers
    assert "/a/test/2" in pointers
    assert "/a/test/3" in pointers
    assert "/a/test/4" in pointers
    assert "/a/test/0/item" in pointers
    assert "/a/test/1/item" in pointers
    assert "/a/test/2/item" in pointers
    assert "/a/test/3/item" in pointers
    assert "/a/test/4/item" in pointers

    assert "/a/key" in pointers
    assert "/a/key/0" in pointers
    assert "/a/key/0/x" in pointers
    assert "/a/key/0/x/2" in pointers
    assert "/a/key/1" in pointers
    assert "/a/key/2" in pointers


def test_are_dumb_strings_equal_not_pluralizable():

    assert are_dumb_strings_equal("'Test'", "'Test'") is True
    assert are_dumb_strings_equal("'Test‘", "Test'") is True


def test_are_dumb_strings_equal_pluralizable():

    assert (
        are_dumb_strings_equal(
            ("'Test'", "Test's"), ("'Test'", "Test's"), pluralizable=True
        )
        is True
    )
    assert (
        are_dumb_strings_equal(
            ("'Test‘", "’Test‘"), ("'Test'", "’Test’"), pluralizable=True
        )
        is True
    )
