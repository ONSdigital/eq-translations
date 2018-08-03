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
        for key in ['description', 'label', 'title', 'question']:
            value = container.get(key)

            if value is not None and value != '':
                if context is not None:
                    extracted_text.append((context, value))
                else:
                    extracted_text.append((key, value))

    elif isinstance(container, list):
        for value in container:
            if context is not None:
                extracted_text.append((context, value))
            else:
                extracted_text.append(('', value))

    return extracted_text


def get_text(data):
    translatable_text = []

    translatable_text.extend(get_text_for_container(data))

    # Now build up translatable text from the nested dictionaries and lists
    for section in data['sections']:
        translatable_text.extend(get_text_for_container(section, section['id']))

        for group in section['groups']:
            translatable_text.extend(get_text_for_container(group, group['id']))

            for block in group['blocks']:
                translatable_text.extend(get_text_for_container(block, block['id']))

                if 'questions' not in block:
                    translatable_text.extend(get_non_question_translatable_text(block))
                    continue

                for question in block['questions']:
                    translatable_text.extend(get_question_translatable_text(question))
                    translatable_text.extend(get_definitions_text(question))

                    for answer in question['answers']:
                        translatable_text.extend(get_text_for_container(answer, answer['id']))
                        translatable_text.extend(get_guidance_text(answer))
                        translatable_text.extend(get_options_text(answer))
                        translatable_text.extend(get_validation_text(answer))

    return translatable_text


def get_non_question_translatable_text(container):
    extracted_text = []
    if container['type'] == 'Introduction':
        extracted_text.extend(get_introduction_translatable_text(container))
    elif container['type'] == 'Interstitial':
        extracted_text.extend(get_interstitial_translatable_text(container))
    elif container['type'] == 'CalculatedSummary':
        extracted_text.extend(get_calculated_summary_translatable_text(container))

    return extracted_text


def get_interstitial_translatable_text(block):
    translatable_text = []

    if 'content' in block:
        translatable_text.extend(get_content_text(block.get('content'), block['id']))
        translatable_text.extend(get_text_for_container(block, block['id']))
    translatable_text.extend(get_text_for_container(block, block['id']))

    return translatable_text

def get_calculated_summary_translatable_text(block):
    translatable_text = []

    translatable_text.extend(get_titles_text(block['titles'], block['id']))
    translatable_text.extend(get_titles_text(block['calculation']['titles'], block['id']))

    return translatable_text


def get_introduction_translatable_text(block):
    translatable_text = []
    primary_content = block.get('primary_content')
    preview_content = block.get('preview_content')
    secondary_content = block.get('secondary_content')

    if primary_content:
        for context in primary_content:
            if 'content' in context:
                translatable_text.extend(get_content_text(context.get('content'), context['id']))

    if preview_content:
        translatable_text.extend(get_preview_content_text(preview_content))

    if secondary_content:
        for context in secondary_content:
            if 'content' in context:
                translatable_text.extend(get_content_text(context.get('content'), context['id']))
                translatable_text.extend(get_text_for_container(context, context['id']))
            translatable_text.extend(get_text_for_container(context, context['id']))

    return translatable_text


def get_preview_content_text(preview_content):
    extracted_text = []

    extracted_text.extend(get_text_for_container(preview_content, preview_content['id']))

    if preview_content.get('content'):
        extracted_text.extend(get_content_text(preview_content['content'], preview_content['id']))
    if preview_content.get('questions'):
        for preview in preview_content['questions']:
            preview_key = preview_content['id']
            extracted_text.extend(get_text_for_container(preview, preview_key))
            extracted_text.extend(get_content_text(preview['content'], preview_key))

    return extracted_text


def get_content_text(container, container_id):
    extracted_text = []
    for index, content in enumerate(container):
        container_key = container_id
        if content.get('list'):
            for value in content['list']:
                extracted_text.append((container_key, value))
                extracted_text.extend((get_text_for_container(content, container_key)))
        extracted_text.extend((get_text_for_container(content, container_key)))

    return extracted_text


def get_question_translatable_text(question):
    extracted_text = []

    extracted_text.extend(get_validation_text(question))
    extracted_text.extend(get_guidance_text(question))

    if 'titles' in question:
        extracted_text.extend(get_titles_text(question['titles'], question['id']))
        extracted_text.extend(get_text_for_container(question, question['id']))
    extracted_text.extend(get_text_for_container(question, question['id']))

    return extracted_text


def get_titles_text(titles, question_id):
    extracted_text = []

    for index, title in enumerate(titles):
        if 'value' in title:
            title_key = question_id
            extracted_text.append((title_key, title['value']))

    return extracted_text


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
            for guide in container['guidance']:
                if 'hide_guidance' in guide:
                    extracted_text.extend(get_show_hide_guidance_text(container['guidance'], container['id'] + ' [question guidance]'))
            for guidance in container['guidance']['content']:
                extracted_text.extend(get_text_for_container(guidance, container['id'] + ' [question guidance]'))

                if 'list' in guidance:
                    extracted_text.extend(get_text_for_container(guidance['list'], container['id'] + ' [question guidance]'))

    return extracted_text


def get_options_text(container):
    extracted_text = []
    if 'options' in container:
        for options in container['options']:
            extracted_text.extend(get_text_for_container(options, container['id']))

    return extracted_text


def get_show_hide_guidance_text(container, container_id):
    extracted_text = []
    for value in container:
        if 'hide_guidance' in value:
            extracted_text.append((container_id, container[value]))
        elif 'show_guidance' in value:
            extracted_text.append((container_id, container[value]))

    return extracted_text


def get_definitions_text(container):
    extracted_text = []
    if 'definitions' in container:
        for value in container['definitions']:
            extracted_text.extend(get_text_for_container(value, container['id']))

    return extracted_text


def sort_text(tuples_to_sort):
    return sorted(tuples_to_sort, key=lambda tup: tup[0], reverse=True)


def remove_duplicates(text_with_duplicates):
    return set(text_with_duplicates)


def output_translations_to_file(text_list, file_name):
    wb = Workbook()
    ws = wb.active
    ws.append(['Context', 'English Text', 'Translated Text'])
    for line in text_list:
        if 'questions' in line[0]:
            ws.append(['', '', ''])
        value = line[1]
        if value == '{{[answers.first_name[group_instance], answers.last_name[group_instance]] |' \
                    ' format_household_name }}' or \
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
    unique_text = remove_duplicates(text)
    sorted_text = sort_text(unique_text)

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
