from eq_translations.utils import (
    find_pointers_containing,
    find_pointers_to,
    json_path_to_json_pointer,
    list_pointers,
    get_message_id,
    get_parent_schema_object,
)


def test_get_message_id():
    pointer_content = "A test title"

    assert get_message_id(pointer_content) == pointer_content


def test_get_message_id_for_plurals():
    pointer_contents = {"one": "Singular text", "other": "Plural text"}

    singular_form = pointer_contents["one"]
    plural_form = pointer_contents["other"]

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


def test_get_parent_schema_object():
    question_schema = {
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

    parent_question = get_parent_schema_object(
        question_schema, "/question/answers/0/options/0/label", "question"
    )
    assert parent_question == question_schema["question"]

    parent_answer = get_parent_schema_object(
        question_schema, "/question/answers/0/options/0/label", "answers"
    )
    assert parent_answer == question_schema["question"]["answers"][0]

    parent_answer_option = get_parent_schema_object(
        question_schema, "/question/answers/0/options/0/label", "options"
    )
    assert (
        parent_answer_option == question_schema["question"]["answers"][0]["options"][0]
    )


def test_json_path_to_json_pointer():
    tests = [
        ("foo", "/foo"),
        ("foo.baz", "/foo/baz"),
        ("foo.[0].baz", "/foo/0/baz"),
        ("foo.[0].baz.qux", "/foo/0/baz/qux"),
        ("foo.[0].baz.[1].qux", "/foo/0/baz/1/qux"),
    ]
    for test in tests:
        assert test[1] == json_path_to_json_pointer(test[0])
