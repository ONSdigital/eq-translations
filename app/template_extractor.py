import argparse
import datetime
import os
from collections import defaultdict
from app.utils import get_output_file_path, deserialise_json


class TemplateExtractor:

    def __init__(self, input_schema_path):
        self.input_schema_path = input_schema_path
        self.schema_data = deserialise_json(input_schema_path)

        self.keys_for_translation = ['description', 'label', 'title', 'question', 'legal_basis']
        self.translation_object = defaultdict()
        self._create_translation_object()

    def _create_translation_object(self):
        if 'legal_basis' in self.schema_data and self.schema_data['legal_basis'] != 'Voluntary':
            self.add_to_translation_object(self.schema_data['legal_basis'])

        # Now build up translatable text from the nested dictionaries and lists
        for section in self.schema_data['sections']:
            self.write_text_for_container(section)

            for group in section['groups']:
                self.write_text_for_container(group)

                for block in group['blocks']:
                    self.write_text_for_container(block)

                    if 'questions' not in block:
                        self.get_non_question_translatable_text(block)

                    for question in block.get('questions', {}):
                        msgctxt = 'Answer for: ' + self.get_title_text_for_context(question)

                        self.write_question_translatable_text(question)

                        for answer in question.get('answers', []):
                            answer_context = ['answer-id: ' + answer['id']]
                            self.write_text_for_container(answer)
                            self.get_guidance_text(answer)
                            self.get_options_text(answer, answer_context, msgctxt)
                            self.get_validation_text(answer)

    def get_title_text_for_context(self, container):
        if 'titles' in container:
            return container['titles'][0]['value']

        return container.get('title', '""')

    def write_text_for_container(self, container, context=None, msgctxt=None):
        if isinstance(container, dict, ):
            for key in self.keys_for_translation:
                value = container.get(key)
                if value is not None and value != '':
                    self.add_to_translation_object(value, context, msgctxt=msgctxt)
        elif isinstance(container, list):
            for value in container:
                self.add_to_translation_object(value, context, msgctxt=msgctxt)

    def add_to_translation_object(self, value, context=None, msgctxt=None):
        object_key = (TemplateExtractor.trim_chars_from_object_key(value),
                      TemplateExtractor.trim_chars_from_object_key(msgctxt))

        if context and self.translation_object.get(object_key):
            context = self.translation_object[object_key]['context'] + context

        self.translation_object[object_key] = {
            'value': value,
            'context': context,
            'msgctxt': msgctxt,
        }

    @staticmethod
    def trim_chars_from_object_key(key_value):
        remove_these_chars = ["'", '“', '”', '‘', '’']

        if key_value:
            for char in remove_these_chars:
                key_value = key_value.replace(char, '')

        return key_value

    def save(self, output_directory):

        output_path = get_output_file_path(self.input_schema_path, output_directory, 'pot')
        print('\nCreating {} from {}'.format(output_path, self.input_schema_path))

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        output_file = open(output_path, 'w', encoding='utf8')
        output = self.get_pot_file_header(output_path)

        for translation in self.translation_object.values():
            if translation['context']:
                for context_item in translation['context']:
                    output += '#: {}\n'.format(context_item)

            if translation.get('msgctxt'):
                output += 'msgctxt "{}"\n'.format(translation['msgctxt'])

            output += 'msgid "{}"\n'.format(translation['value'])
            output += 'msgstr ""\n\n'

        output_file.write(output)
        output_file.close()

    def get_pot_file_header(self, output_path):
        header = '# Translation POT file for: ' + output_path.split('/')[-1] + '\n' \
                 '#, fuzzy\n' \
                 'msgid ""\n' \
                 'msgstr ""\n' \
                 '"Project-Id-Version: eq-translations\\n"\n' \
                 '"POT-Creation-Date: ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p") + '\\n"\n' \
                 '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' \
                 '"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' \
                 '"Language-Team: LANGUAGE <LL@li.org>\\n"\n' \
                 '"MIME-Version: 1.0\\n"\n' \
                 '"Content-Type: text/plain; charset=utf-8\\n"\n' \
                 '"Content-Transfer-Encoding: 8bit\\n"\n\n'

        return header

    def get_non_question_translatable_text(self, container):
        if container['type'] == 'Introduction':
            self.get_introduction_translatable_text(container)
        elif container['type'] == 'Interstitial':
            self.get_interstitial_translatable_text(container)
        elif container['type'] == 'CalculatedSummary':
            self.get_calculated_summary_translatable_text(container)
        elif container['type'] == 'Content':
            self.write_text_for_container(container)

    def get_interstitial_translatable_text(self, block):
        if 'content' in block:
            self.get_content_text(block.get('content'))

    def get_calculated_summary_translatable_text(self, block):
        self.get_titles_text(block['titles'])
        self.get_titles_text(block['calculation']['titles'])

    def get_introduction_translatable_text(self, block):
        for content in block.get('primary_content', []):
            if 'content' in content:
                self.get_content_text(content['content'])
            self.write_text_for_container(content)

        if 'preview_content' in block:
            self.get_preview_content_text(block['preview_content'])

        for content in block.get('secondary_content', []):
            if 'content' in content:
                self.get_content_text(content['content'])
            self.write_text_for_container(content)

    def get_preview_content_text(self, preview_content):
        self.write_text_for_container(preview_content)

        if preview_content.get('content'):
            self.get_content_text(preview_content['content'])
        if preview_content.get('questions'):
            for preview in preview_content['questions']:
                self.write_text_for_container(preview)
                self.get_content_text(preview['content'])

    def get_content_text(self, container, msgctxt=None):
        for index, content in enumerate(container):
            self.write_text_for_container(content, msgctxt=msgctxt)
            if not isinstance(content, str) and content.get('list'):
                for value in content['list']:
                    self.add_to_translation_object(value)
                    self.write_text_for_container(value, msgctxt=msgctxt)

    def write_question_translatable_text(self, question):
        if 'title' in question:
            self.add_to_translation_object(question['title'])
        elif 'titles' in question:
            self.get_titles_text(question['titles'])

        if 'description' in question:
            self.add_to_translation_object(question['description'])

        self.get_guidance_text(question)
        self.get_definitions_text(question)
        self.get_validation_text(question)

        if question['type'] == 'Content':
            self.write_text_for_container(question)

    def get_titles_text(self, titles):
        for index, title in enumerate(titles):
            if 'value' in title:
                self.add_to_translation_object(title['value'])

    def get_validation_text(self, container):
        if 'validation' in container:
            for value in container['validation']['messages'].values():
                self.add_to_translation_object(value)

    def get_guidance_text(self, container):
        if 'guidance' in container:
            guidance_text = container['guidance']
            if isinstance(guidance_text, str):
                self.add_to_translation_object(container['guidance'])
            else:
                self.get_show_hide_guidance_text(container['guidance'])
                self.get_content_text(container['guidance']['content'])

    def get_options_text(self, container, context, msgctxt=None):
        for option in container.get('options', []):
            self.write_text_for_container(option, context, msgctxt=msgctxt)
            if 'detail_answer' in option:
                self.write_text_for_container(option['detail_answer'], context, msgctxt=msgctxt)

    def get_show_hide_guidance_text(self, container):
        if 'show_guidance' in container:
            self.add_to_translation_object(container['show_guidance'])
        if 'hide_guidance' in container:
            self.add_to_translation_object(container['hide_guidance'])

    def get_definitions_text(self, container, msgctxt=None):
        if 'definitions' in container:
            for definition in container['definitions']:
                if 'title' in definition:
                    self.write_text_for_container(definition, msgctxt=msgctxt)
                    self.get_content_text(definition['content'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract translation template from json schema")

    parser.add_argument(
        'SCHEMA_PATH',
        help="The path to the source schema from which data will be extracted"
    )

    parser.add_argument(
        'OUTPUT_DIRECTORY',
        help="The destination directory for the translation template"
    )

    args = parser.parse_args()

    template_extractor = TemplateExtractor(args.SCHEMA_PATH)
    template_extractor.save(args.OUTPUT_DIRECTORY)
