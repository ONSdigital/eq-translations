from eq_translations.utils import (
    find_pointers_containing,
    find_pointers_to,
    list_pointers,
    get_message_id,
)


def test_get_message_id():
    pointer_content = "A test title"

    assert get_message_id(pointer_content) == pointer_content


def test_get_message_id_for_plurals():
    pointer_contents = {
        "forms": {"one": "Singular text", "other": "Plural text"},
    }

    singular_form = pointer_contents["forms"]["one"]
    plural_form = pointer_contents["forms"]["other"]

    assert get_message_id(pointer_contents) == (singular_form, plural_form)


def test_find_pointers_containing_root():
    schema = {"test": ""}

    pointers = list(find_pointers_containing(schema, "test"))

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
