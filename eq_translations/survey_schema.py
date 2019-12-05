import json
import copy

from babel.messages import Catalog
from jsonpointer import resolve_pointer, set_pointer

from eq_translations.utils import find_pointers_to, get_parent_pointer, dumb_to_smart_quotes, is_placeholder


class SurveySchema:
    schema = {}
    no_context_keys = [
        'show_guidance',
        'hide_guidance',
        'legal_basis',
        'playback',
        'item_title',
        'add_link_text',
        'empty_list_text',
        'instruction',
    ]
    context_placeholder_pointers = []
    no_context_placeholder_pointers = []

    def __init__(self, schema_data=None):
        self.schema = schema_data
        self.load_placeholders()

    def load(self, schema_path):
        with open(schema_path, encoding='utf8') as schema_file:
            self.schema = json.load(schema_file)
            self.load_placeholders()

    def load_placeholders(self):
        if self.schema:
            self.context_placeholder_pointers, self.no_context_placeholder_pointers = self.get_placeholder_pointers()

    def save(self, schema_path):
        with open(schema_path, 'w', encoding='utf8') as schema_file:
            return json.dump(self.schema, schema_file, indent=4)

    @property
    def pointers(self):
        return self.no_context_pointers + self.context_pointers

    @property
    def no_context_pointers(self):
        return (
            self.get_core_pointers()
            + self.get_title_pointers()
            + self.get_message_pointers()
            + self.get_list_pointers()
            + self.get_schema_description_pointer()
            + self.no_context_placeholder_pointers

        )

    @property
    def context_pointers(self):
        return self.get_answer_pointers() + self.get_description_pointers() + self.context_placeholder_pointers

    def get_core_pointers(self):
        """
        Iterate the schema and return the pointers found
        :return:
        """
        pointers = []
        for key in SurveySchema.no_context_keys:
            key_pointers = find_pointers_to(self.schema, key)
            pointers.extend(key_pointers)
        return pointers

    def get_schema_description_pointer(self):
        return [[key_pointer for key_pointer in find_pointers_to(self.schema, 'description')][0]]

    def get_placeholder_pointers(self):
        """
        Placeholder pointers may have context or may not
        :return:
        """
        found_pointers = find_pointers_to(self.schema, 'text')
        context_placeholder_pointers = []
        no_context_placeholder_pointers = []

        for pointer in found_pointers:
            if '/answers/' in pointer:
                context_placeholder_pointers.append(pointer)
            else:
                no_context_placeholder_pointers.append(pointer)

        return context_placeholder_pointers, no_context_placeholder_pointers

    def get_message_pointers(self):
        """
        Message pointers need to be iterated as a dict and each key added individually
        :return:
        """
        pointers = []

        message_pointers = find_pointers_to(self.schema, 'messages')
        for message_pointer in message_pointers:
            schema_element = resolve_pointer(self.schema, message_pointer)
            for element in schema_element:
                pointers.append(f'{message_pointer}/{element}')
        return pointers

    def get_list_pointers(self):
        """
        List pointers need to be iterated and each element added individually
        :return:
        """
        pointers = []

        list_pointers = find_pointers_to(self.schema, 'list')
        for list_pointer in list_pointers:
            schema_element = resolve_pointer(self.schema, list_pointer)
            if isinstance(schema_element, list):
                pointers.extend(
                    [f'{list_pointer}/{i}' for i, p in enumerate(schema_element)]
                )
        return pointers

    def get_title_pointers(self):
        """
        Titles need to be handled separately as they may require context for translation
        """
        return find_pointers_to(self.schema, 'title')

    def get_answer_pointers(self):
        """
        Labels for options/answers need to be handled separately as they require context
        """
        return find_pointers_to(self.schema, 'label')

    def get_description_pointers(self):
        return find_pointers_to(self.schema, 'description')[1:]

    def get_parent_id(self, pointer):
        resolved_data = resolve_pointer(self.schema, pointer)

        if isinstance(resolved_data, dict) and 'id' in resolved_data:
            return resolved_data['id']

        parent_pointer = get_parent_pointer(pointer)
        return self.get_parent_id(parent_pointer)

    @staticmethod
    def get_parent_question_pointer(pointer):
        pointer_parts = pointer.split('/')

        if 'question' in pointer_parts:
            pointer_index = pointer_parts.index('question')
            return '/'.join(pointer_parts[:pointer_index + 1])

    def get_parent_question(self, pointer):
        question_pointer = self.get_parent_question_pointer(pointer) or ''
        if question_pointer is None:
            question_pointer = ''
        return resolve_pointer(self.schema, question_pointer + '/title')

    def get_catalog(self):
        """
        :return: a schema catalog to be used as the content within a po/pot file
        """
        catalog = Catalog()
        total_translations = len(self.no_context_pointers + self.context_pointers)

        for pointer in self.no_context_pointers:
            pointer_contents = resolve_pointer(self.schema, pointer)
            if pointer_contents:
                catalog.add(dumb_to_smart_quotes(pointer_contents))

        for pointer in self.context_pointers:
            pointer_contents = resolve_pointer(self.schema, pointer)
            if pointer_contents:
                parent_answer_id = self.get_parent_id(pointer)
                question = self.get_parent_question(pointer)

                message_context = 'Answer for: {}'.format(question['text'] if is_placeholder(question) else question)

                catalog.add(
                    dumb_to_smart_quotes(pointer_contents),
                    context=message_context,
                    auto_comments=[f'answer-id: {parent_answer_id}'],
                )

        print(f'Total Messages: {total_translations}')

        return catalog

    def translate(self, schema_translation):
        """
        Use the supplied schema translation object to translate pointers found
        within the survey

        :param schema_translation:
        :return:
        """
        translated_schema = copy.deepcopy(self.schema)
        total_translations = len(self.no_context_pointers + self.context_pointers)
        missing_translations = 0

        for pointer in self.no_context_pointers:
            pointer_contents = resolve_pointer(self.schema, pointer)
            if pointer_contents:
                translation = schema_translation.translate_message(pointer_contents)
                if translation:
                    translated_schema = set_pointer(translated_schema, pointer, translation)
                else:
                    missing_translations += 1
                    print(
                        "Missing translation at {}: '{}'".format(pointer, pointer_contents)
                    )

        for pointer in self.context_pointers:
            pointer_contents = resolve_pointer(self.schema, pointer)
            if pointer_contents:
                parent_answer_id = self.get_parent_id(pointer)
                question = self.get_parent_question(pointer)
                message_context = 'Answer for: {}'.format(question['text'] if is_placeholder(question) else question)
                translation = schema_translation.translate_message(
                    pointer_contents, parent_answer_id, message_context
                )
                if translation:
                    translated_schema = set_pointer(translated_schema, pointer, translation)
                else:
                    missing_translations += 1
                    print(
                        f"Missing translation at {pointer}: \'{pointer_contents}\'"
                    )

        print(f'\nTotal Messages: {total_translations}')

        if missing_translations:
            print(f'Total Missing: {missing_translations}')

        return SurveySchema(translated_schema)
