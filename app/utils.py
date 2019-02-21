import json
import os
import re


def deserialise_json(json_file_to_deserialise):
    with open(json_file_to_deserialise, 'r', encoding="utf8") as json_data:
        try:
            data = json.load(json_data)
            return data

        except ValueError:
            print("Error decoding JSON. Please ensure file is in valid JSON format.")
            return None


def get_output_file_path(schema_path, output_directory, output_format):
    file_name = os.path.splitext(os.path.basename(schema_path))[0]
    output_file = file_name + '.' + output_format
    output_path = os.path.join(output_directory, output_file)

    return output_path


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
