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
            yield pointer + '/' + k if pointer else '/' + k
            yield from list_pointers(v, pointer + '/' + k if pointer else '/' + k)
    elif isinstance(input_data, list) and input_data:
        for index, item in enumerate(input_data):
            yield '{}/{}'.format(pointer, index) if pointer else '/{}'.format(index)
            yield from list_pointers(item, '{}/{}'.format(pointer, index))


def compare_schemas(source_schema, target_schema):
    """
    Compare the pointers in two json structures and return differences
    :param source_schema: Structure to identify differences against
    :param target_schema: Target structure to compare against
    :return:
    """
    source_survey_pointers = set(list_pointers(source_schema))
    target_survey_pointers = set(list_pointers(target_schema))

    missing_target_pointers = source_survey_pointers.difference(target_survey_pointers)
    missing_source_pointers = target_survey_pointers.difference(source_survey_pointers)

    missing_pointers = missing_target_pointers | missing_source_pointers

    for list_pointer in missing_pointers:
        print('Missing Pointer: {}'.format(list_pointer))

    print('\nTotal attributes in source schema: {}'.format(len(source_survey_pointers)))
    print('Total attributes in target schema: {}'.format(len(target_survey_pointers)))
    print('Differences between source/target schema attributes: {} '.format(len(missing_pointers)))

    return missing_pointers


def is_placeholder(input_data):
    return 'placeholders' in input_data


def find_pointers_containing(input_data, search_key, pointer=None):
    """
    Recursive function which lists pointers which contain a search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the current pointer
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if pointer and search_key in input_data and not is_placeholder(input_data[search_key]):
            yield pointer
        for k, v in input_data.items():
            yield from find_pointers_containing(v, search_key, pointer + '/' + k if pointer else '/' + k)
    elif isinstance(input_data, list):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(item, search_key, '{}/{}'.format(pointer, index))


def find_pointers_to(input_data, search_key):
    """
    Find pointers to a particular search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :return: list of the json pointer paths
    """
    root_pointers = ['/{}'.format(search_key)] if search_key in input_data and not is_placeholder(input_data[search_key]) else []
    pointer_iterator = find_pointers_containing(input_data, search_key)
    return root_pointers + ['{}/{}'.format(p, search_key) for p in pointer_iterator]


def get_parent_pointer(pointer):
    pointer_parts = pointer.split('/')

    if len(pointer_parts) > 2:
        return '/'.join(pointer_parts[:-1])


def dumb_to_smart_quotes(string):
    """Takes a string and returns it with dumb quotes, single and double,
    replaced by smart quotes. Accounts for the possibility of HTML tags
    within the string.
    From https://gist.github.com/davidtheclark/5521432"""

    # Find dumb single quotes coming directly after letters or punctuation,
    # and replace them with right single quotes.
    string = re.sub(r'([\w.,?!;:\"\'])\'', r'\1’', string)
    # Find any remaining dumb single quotes and replace them with
    # left single quotes.
    string = string.replace("'", '‘')
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around HTML
    # attributes (following =) and replace them with dumb quotes.
    string = re.sub(r'=‘(.*?)’', r"='\1'", string)
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around Jinja
    # attributes (following [) and replace them with dumb quotes.
    string = re.sub(r'\[‘(.*?)’', r"['\1'", string)
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around date
    # parameters passed to Jinja filters and replace them with dumb quotes.
    string = re.sub(r'‘(MO|TU|WE|TH|FR|SA|SU|EEEE d MMMM YYYY|EEEE dd MMMM|EEEE d MMMM|weeks)’', r"'\1'", string)

    return string.strip()


L_SQUOTE = '\u2018'
R_SQUOTE = '\u2019'
L_DQUOTE = '\u201C'
R_DQUOTE = '\u201D'


def remove_quotes(message):
    message = re.sub(fr'[{L_DQUOTE}|{R_DQUOTE}|{L_SQUOTE}|{R_DQUOTE}]', '', message)

    return message.strip()


def are_dumb_strings_equal(message_a, message_b):
    return remove_quotes(message_a) == remove_quotes(message_b)
