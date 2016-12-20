# TODO
"""
- Get unit tests set up for running of script (e.g. against different JSON, outputs etc)

- Get values from dict recursively instead of multiple nested loops?

- Think of better way to handle intermittent keys in get_conditional_text_for_container().

- Add/amend other team/best practice stuff that's been missed out.
"""

import json
import os
import sys
from openpyxl import Workbook

OUTPUT_FILE_EXTENSION = "_translate.xlsx"


def get_text_for_container(container, context=None):

    extracted_text = []

    if isinstance(container, dict):
        for key in ['description', 'label', 'title']:
            value = container.get(key)

            if value is not None and value != '':
                if context is not None:
                    extracted_text.append((context, value))
                else:
                    extracted_text.append(('', value))

    elif isinstance(container, list):
        for value in container:
            if context is not None:
                extracted_text.append((context, value))
            else:
                extracted_text.append(('', value))

    return extracted_text


def get_text(data):
    translatable_text = []

    # Get header section text
    # translatable_text.extend(get_text_for_container(data))
    # translatable_text.extend(get_conditional_text_for_container(data))

    # Now build up translatable text from the nested dictionaries and lists
    for group in data['groups']:
        # translatable_text.extend(get_text_for_container(group))

        for block in group['blocks']:
            # translatable_text.extend(get_text_for_container(block))

            for section in block['sections']:
                translatable_text.extend(get_text_for_container(section, section['id']))

                for question in section['questions']:
                    translatable_text.extend(get_text_for_container(question, question['id']))
                    translatable_text.extend(get_validation_text(question))
                    translatable_text.extend(get_guidance_text(question))

                    for answer in question['answers']:
                        translatable_text.extend(get_text_for_container(answer, answer['id']))
                        translatable_text.extend(get_guidance_text(answer))
                        translatable_text.extend(get_options_text(answer))
                        translatable_text.extend(get_validation_text(answer))

    return translatable_text


def get_validation_text(container):
    extracted_text = []
    if 'validation' in container:
        for value in container['validation']['messages'].values():
            context = container['id'] + ' [validation message]'
            extracted_text.append((context, value))

    return extracted_text


def get_guidance_text(container):
    extracted_text = []
    if 'guidance' in container:

        guidance_text = container['guidance']

        if isinstance(guidance_text, str):
            extracted_text.append((container['id'] + ' [answer guidance]', container['guidance']))
        else:
            for guidance in container['guidance']:
                extracted_text.extend(get_text_for_container(guidance, container['id'] + ' [question guidance]'))

                if 'list' in guidance:
                    extracted_text.extend(get_text_for_container(guidance['list'], container['id'] + ' [question guidance]'))

    return extracted_text


def get_options_text(container):
    extracted_text = []
    if 'options' in container:
        for options in container['options']:
            extracted_text.extend(get_text_for_container(options, container['id']))

            if 'other' in options:
                extracted_text.extend(get_text_for_container(options['other'], container['id']))

    return extracted_text


def get_introduction_text(container):
    extracted_text = []
    if 'introduction' in container:
        if 'description' in container['introduction']:
            extracted_text.append(container['introduction']['description'])

        if 'information_to_provide' in container['introduction']:
            for value in container['introduction']['information_to_provide']:
                extracted_text.append(value)

    return extracted_text


def sort_text(tuples_to_sort):
    return sorted(tuples_to_sort, key=lambda tup: tup[0], reverse=True)


def remove_duplicates(text_with_duplicates):
    return set(text_with_duplicates)


def output_text_to_file(text_list, file_name):
    with open(file_name, 'w', encoding="utf8") as output_file:

        for line in text_list:
            output_file.write("%s" % line + TEXT_SEPARATOR + line.upper() + "\r\n")


def output_translations_to_file(text_list, file_name):
    wb = Workbook()
    ws = wb.active
    ws.append(['Context', 'English Text', 'Welsh Text'])
    for line in text_list:
        if 'section' in line[0]:
            ws.append(['', '', ''])
        value = line[1]
        if value == '{{[answers.first_name[group_instance], answers.last_name[group_instance]] | format_household_name }}' or \
                value == '{{[answers.first_name, answers.last_name] | format_household_name }}':
            value = ''
        ws.append([line[0], value, ' '])
    wb.save(file_name)


def strip_directory_and_extension(file):
    file_basename = os.path.basename(file)
    file_name = os.path.splitext(file_basename)[0]

    return file_name


def create_output_file_name_with_directory(output_directory, json_file):
    file_name = strip_directory_and_extension(json_file)
    file_name_with_extension = file_name + OUTPUT_FILE_EXTENSION
    file_name_with_directory = os.path.join(output_directory, file_name_with_extension)

    return file_name_with_directory


def deserialise_json(json_file_to_deserialise):
    with open(json_file_to_deserialise, 'r', encoding="utf8") as json_data:
        try:
            data = json.load(json_data)
            return data

        except ValueError:
            print("Error decoding JSON. Please ensure file is in valid JSON format.")
            return None


def command_line_handler(json_file, output_directory):

    print('Creating list of translatable text from: ' + json_file)
    deserialised_json = deserialise_json(json_file)

    if deserialised_json is None:
        exit(1)

    text = get_text(deserialised_json)

    print('Removing duplicate text...')
    # unique_text = remove_duplicates(text)
    sorted_text = sort_text(text)

    print('Outputting text to file...')
    output_file_name = create_output_file_name_with_directory(output_directory, json_file)
    output_translations_to_file(sorted_text, output_file_name)

    print('Finished successfully.')
    print()
    print('Translated text output: ' + output_file_name)
    print()
    exit(0)


if __name__ == '__main__':

    json_file = sys.argv[1]
    output_directory = sys.argv[2]


    command_line_handler(json_file, output_directory)
