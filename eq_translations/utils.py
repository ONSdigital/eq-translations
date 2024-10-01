import re

from jsonpointer import resolve_pointer


def list_pointers(input_data, pointer=None):
    """
    Recursive function which lists all available pointers in a json structure
    :param input_data: the input data to search
    :param pointer: the current pointer
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict) and input_data:
        for k, v in input_data.items():
            yield pointer + "/" + k if pointer else "/" + k
            yield from list_pointers(v, pointer + "/" + k if pointer else "/" + k)
    elif isinstance(input_data, list) and input_data:
        for index, item in enumerate(input_data):
            yield f"{pointer}/{index}" if pointer else f"/{index}"
            yield from list_pointers(item, f"{pointer}/{index}")


def find_pointers_containing(input_data, search_key, pointer=None):
    """
    Recursive function which lists pointers which contain a search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the current pointer
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if pointer and search_key in input_data:
            yield pointer
        for k, v in input_data.items():
            yield from find_pointers_containing(
                v, search_key, f"{pointer}/{k}" if pointer else f"/{k}"
            )
    elif isinstance(input_data, list):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(item, search_key, f"{pointer}/{index}")


def find_pointers_to(input_data, search_key):
    """
    Find pointers to a particular search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :return: list of the json pointer paths
    """
    root_pointers = [f"/{search_key}"] if search_key in input_data else []
    pointer_iterator = find_pointers_containing(input_data, search_key)
    return root_pointers + [f"{pointer}/{search_key}" for pointer in pointer_iterator]


def get_parent_schema_object(input_data, json_pointer, parent_property):
    """
    Get the parent schema object identified by parent_property in the json pointer.
    If the parent schema object is an array then the matching array item is returned.
    :param input_data: the input data to search
    :param json_pointer: the pointer being searched
    :param parent_property: the parent property to search for
    :return: schema object identified by parent_property
    """
    pointer_parts = json_pointer.split("/")
    pointer_index = pointer_parts.index(parent_property)
    parent_pointer = "/".join(pointer_parts[: pointer_index + 1])
    schema_object = resolve_pointer(input_data, parent_pointer)
    if isinstance(schema_object, list):
        return schema_object[int(pointer_parts[pointer_index + 1])]
    return schema_object


def json_path_to_json_pointer(json_path):
    """
    Convert a json path string into a json pointer string.
    :param json_path: the input data to search
    :return: json pointer equivalent to the json path
    """
    json_pointer = json_path.replace("[", "").replace("]", "").replace(".", "/")
    return f"/{json_pointer}"


def dumb_to_smart_quotes(string):
    """Takes a string and returns it with dumb quotes, single and double,
    replaced by smart quotes. Accounts for the possibility of HTML tags
    within the string.
    From https://gist.github.com/davidtheclark/5521432"""

    # Find dumb single quotes coming directly after letters or punctuation,
    # and replace them with right single quotes.
    string = re.sub(r"([\w.,?!;:\"\'])\'", r"\1’", string)
    # Find any remaining dumb single quotes and replace them with
    # left single quotes.
    string = string.replace("'", "‘")
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around HTML
    # attributes (following =) and replace them with dumb quotes.
    string = re.sub(r"=‘(.*?)’", r"='\1'", string)

    # Now repeat the steps above for double quotes
    string = re.sub(r'([\w.,?!;:\\"\'])\"', r"\1”", string)

    string = string.replace('"', "“")
    string = re.sub(r"=“(.*?)”", r"='\1'", string)

    return string


def get_message_id(content):
    if isinstance(content, dict):
        return content.get("one"), content.get("other")

    return content


def get_plural_forms_for_language(language_code):
    mappings = {
        "en": ["one"],
        "cy": ["zero", "one", "two", "few", "many"],
    }

    return mappings[language_code] + ["other"]
