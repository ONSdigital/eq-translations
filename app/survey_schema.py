from babel.messages import Catalog

import json

from app.utils import find_pointers_to, get_parent_pointer, dumb_to_smart_quotes
from jsonpointer import resolve_pointer, set_pointer


class SurveySchema:
    schema = {}
    no_context_keys = [
        'show_guidance',
        'hide_guidance',
        'description',
        'legal_basis',
        'text',
    ]

    def __init__(self, schema_data=None):
        self.schema = schema_data

    def load(self, schema_path):
        with open(schema_path, encoding='utf8') as schema_file:
            self.schema = json.load(schema_file)

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
        )

    @property
    def context_pointers(self):
        return self.get_answer_pointers()

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

    def get_message_pointers(self):
        """
        Message pointers need to be iterated as a dict and each key added individually
        :return:
        """
        pointers = []

        message_pointers = find_pointers_to(self.schema, 'messages')
        for message_pointer in message_pointers:
            schema_element = resolve_pointer(self.schema, message_pointer)
            for k, v in schema_element.items():
                pointers.append("{}/{}".format(message_pointer, k))
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
            pointers.extend(
                ["{}/{}".format(list_pointer, i) for i, p in enumerate(schema_element)]
            )
        return pointers

    def get_title_pointers(self):
        """
        Titles need to be handled separately as they may require context for translation
        :return:
        """
        return find_pointers_to(self.schema, 'title')

    def get_answer_pointers(self):
        """
        Labels for options/answers need to be handled separately as they require context
        :return:
        """
        return find_pointers_to(self.schema, 'label')

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
        question_pointer = self.get_parent_question_pointer(pointer)
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

                user_context = 'Answer for: {}'.format(question)

                catalog.add(
                    dumb_to_smart_quotes(pointer_contents),
                    context=user_context,
                    auto_comments=["answer-id: {}".format(parent_answer_id)],
                )

        print("Total Messages: {}".format(total_translations))

        return catalog

    def translate(self, schema_translation):
        """
        Use the supplied schema translation object to translate pointers found
        within the survey

        :param schema_translation:
        :return:
        """
        translated_schema = self.schema.copy()
        total_translations = len(self.no_context_pointers + self.context_pointers)
        missing_translations = 0

        for pointer in self.no_context_pointers:
            pointer_contents = resolve_pointer(self.schema, pointer)
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
            parent_answer_id = self.get_parent_id(pointer)
            translation = schema_translation.translate_message(
                pointer_contents, parent_answer_id
            )
            if translation:
                translated_schema = set_pointer(translated_schema, pointer, translation)
            else:
                missing_translations += 1
                print(
                    "Missing translation at {}: '{}'".format(pointer, pointer_contents)
                )

        print("\nTotal Messages: {}".format(total_translations))

        if missing_translations:
            print("Total Missing: {}".format(missing_translations))

        return SurveySchema(translated_schema)
