import re


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
            yield "{}/{}".format(pointer, index) if pointer else "/{}".format(index)
            yield from list_pointers(item, "{}/{}".format(pointer, index))


def is_placeholder(input_data):
    return "placeholders" in input_data


def find_pointers_containing(input_data, search_key, pointer=None):
    """
    Recursive function which lists pointers which contain a search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the current pointer
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if (
            pointer
            and search_key in input_data
            and not is_placeholder(input_data[search_key])
        ):
            yield pointer
        for k, v in input_data.items():
            yield from find_pointers_containing(
                v, search_key, pointer + "/" + k if pointer else "/" + k
            )
    elif isinstance(input_data, list):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(
                item, search_key, "{}/{}".format(pointer, index)
            )


def find_pointers_to(input_data, search_key):
    """
    Find pointers to a particular search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :return: list of the json pointer paths
    """
    root_pointers = (
        ["/{}".format(search_key)]
        if search_key in input_data and not is_placeholder(input_data[search_key])
        else []
    )
    pointer_iterator = find_pointers_containing(input_data, search_key)
    return root_pointers + ["{}/{}".format(p, search_key) for p in pointer_iterator]


def get_parent_pointer(pointer):
    pointer_parts = pointer.split("/")

    if len(pointer_parts) > 2:
        return "/".join(pointer_parts[:-1])


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
    # pylint: disable=invalid-string-quote
    string = re.sub(r'([\w.,?!;:\\"\'])\"', r"\1”", string)

    string = string.replace('"', "“")
    string = re.sub(r"=“(.*?)”", r"='\1'", string)

    return string


def remove_quotes(message):
    quotation_marks = [
        "\N{APOSTROPHE}",
        "\N{LEFT SINGLE QUOTATION MARK}",
        "\N{RIGHT SINGLE QUOTATION MARK}",
        "\N{LEFT DOUBLE QUOTATION MARK}",
        "\N{RIGHT DOUBLE QUOTATION MARK}",
    ]
    for char in quotation_marks:
        message = message.replace(char, "")

    return message.strip()


def are_dumb_strings_equal(message_a, message_b, pluralizable=False):
    if pluralizable:
        return {remove_quotes(msg) for msg in message_a} == {
            remove_quotes(msg) for msg in message_b
        }

    return remove_quotes(message_a) == remove_quotes(message_b)


def get_message_id_for_plural_forms(forms):
    singular = forms["one"]
    plural = forms["other"]

    return dumb_to_smart_quotes(singular), dumb_to_smart_quotes(plural)


def get_message_id(content):
    if "forms" in content:
        return get_message_id_for_plural_forms(content["forms"])

    return dumb_to_smart_quotes(content)


def get_plural_forms_for_language(language_code):
    mappings = {
        "en": ["one"],
        "cy": ["zero", "one", "two", "few", "many"],
        "ga": ["one", "two", "few", "many"],
        "eo": ["one"],
    }

    return mappings[language_code] + ["other"]
