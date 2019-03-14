import re


def find_pointers_containing(input_data, search_key, pointer=None):
    """
    Recursive function which lists pointers which contain a search key
    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the key to search for
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if pointer and search_key in input_data:
            yield pointer
        for k, v in input_data.items():
            if isinstance(v, dict) and search_key in v:
                yield pointer + '/' + k if pointer else '/' + k
            else:
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
    root_pointers = ['/{}'.format(search_key)] if search_key in input_data else []
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
    string = re.sub(r"([\w.,?!;:\"\'])'", r'\1’', string)
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
