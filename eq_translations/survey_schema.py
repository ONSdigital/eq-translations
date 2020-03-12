import copy
import json

from babel.messages import Catalog
from jsonpointer import resolve_pointer, set_pointer

from eq_translations.utils import (
    find_pointers_to,
    get_message_id,
    dumb_to_smart_quotes,
    get_plural_forms_for_language,
)


class SurveySchema:
    schema = {}
    keys_with_context = ["playback", "title", "label"]
    keys_to_translate = [
        "show_guidance",
        "hide_guidance",
        "description",
        "legal_basis",
        "item_title",
        "add_link_text",
        "empty_list_text",
        "instruction",
        "cancel_text",
        "list",
        "messages",
    ] + keys_with_context

    def __init__(self, schema_data=None):
        self.schema = schema_data

    def load(self, schema_path):
        with open(schema_path, encoding="utf8") as schema_file:  # pragma: no cover
            self.schema = json.load(schema_file)  # pragma: no cover

    def save(self, schema_path):
        with open(schema_path, "w", encoding="utf8") as schema_file:  # pragma: no cover
            return json.dump(self.schema, schema_file, indent=4)  # pragma: no cover

    @property
    def translatable_items(self):
        """
        :yield: A pointer dictionary
        :return: A generator
        """

        for key in self.keys_to_translate:
            with_context = key in self.keys_with_context

            for pointer in find_pointers_to(self.schema, key):
                # The 'list' property is used by both 'contents' and 'when' blocks.
                if "/when/" in pointer:
                    continue

                schema_element = resolve_pointer(self.schema, pointer)
                if isinstance(schema_element, dict):
                    yield from self._get_translatable_items_from_dict_element(
                        pointer, schema_element, with_context
                    )

                elif isinstance(schema_element, list):
                    yield from self._get_translatable_items_from_list_element(
                        pointer, schema_element, with_context
                    )

                else:
                    yield self._get_translatable_item(
                        pointer, schema_element, with_context
                    )

    def _get_translatable_items_from_dict_element(
        self, pointer, schema_element, with_context
    ):
        plural_forms = schema_element.get("text_plural", {}).get("forms")
        if plural_forms:
            plural_forms_pointer = f"{pointer}/text_plural/forms"
            yield self._get_translatable_item(
                plural_forms_pointer, plural_forms, with_context
            )

        for element, value in schema_element.items():
            if isinstance(value, str):
                element_pointer = f"{pointer}/{element}"
                yield self._get_translatable_item(element_pointer, value, with_context)

    def _get_translatable_items_from_list_element(
        self, pointer, schema_element, with_context
    ):
        for index, value in enumerate(schema_element):
            if isinstance(value, str):
                list_item_pointer = f"{pointer}/{index}"
                yield self._get_translatable_item(
                    list_item_pointer, value, with_context
                )

    def _get_translatable_item(self, pointer, value=None, with_context=False):
        """
        :param pointer: Defines a string syntax for identifying a specific value within the schema.
        :param value: The resolved value of the pointer. This is a Tuple for plural forms, and a String for all other elements
        :param with_context: Boolean flag to signify whether this pointer should have the question title as context.
        :return: A dictionary.
        """
        pointer_dict = {"pointer": pointer, "value": value}

        if with_context and f"/answers/" in pointer:
            context = self._get_context_from_pointer(pointer)
            pointer_dict["context"] = context

        return pointer_dict

    @staticmethod
    def _get_parent_question_pointer(pointer):
        pointer_parts = pointer.split("/")

        if "question" in pointer_parts:
            pointer_index = pointer_parts.index("question")
            return "/".join(pointer_parts[: pointer_index + 1])

    def get_parent_question(self, pointer):
        question_pointer = self._get_parent_question_pointer(pointer)
        return resolve_pointer(self.schema, question_pointer + "/title")

    def _get_context_from_pointer(self, pointer):
        question = self.get_parent_question(pointer)

        if "text_plural" in question:
            context = question["text_plural"]["forms"]["other"]
        elif "placeholders" in question:
            context = question["text"]
        else:
            context = question

        return f"Answer for: {context}"

    @property
    def catalog(self):
        """
        :return: a schema catalog to be used as the content within a po/pot file
        """
        catalog = Catalog()

        translatable_items = list(self.translatable_items)

        for translatable_item in translatable_items:
            context = translatable_item.get("context")
            value = translatable_item["value"]

            if not value:
                continue

            message_id = get_message_id(value)
            catalog.add(
                id=message_id, context=context,
            )

        print(f"Total Messages: {len(translatable_items)}")

        return catalog

    def translate(self, schema_translation, language_code):
        """
        Use the supplied schema translation object and language code to translate pointers found
        within the survey

        :param schema_translation: The SchemaTranslation object
        :param language_code: The target language code
        :return:
        """
        translated_schema = copy.deepcopy(self.schema)
        missing_translations = 0

        translatable_items = list(self.translatable_items)

        for translatable_item in translatable_items:
            pointer = translatable_item["pointer"]
            value = translatable_item["value"]

            if not value:
                continue

            message_id = get_message_id(value)
            context = translatable_item.get("context")

            translation = schema_translation.get_translation(message_id, context)

            if translation:
                if isinstance(translation, tuple) and language_code:
                    plural_forms = get_plural_forms_for_language(language_code)
                    for index, plural_form in enumerate(plural_forms):
                        plural_form_pointer = f"{pointer}/{plural_form}"
                        set_pointer(
                            translated_schema,
                            plural_form_pointer,
                            dumb_to_smart_quotes(translation[index]),
                        )
                else:
                    set_pointer(
                        translated_schema, pointer, dumb_to_smart_quotes(translation),
                    )
            else:
                print(f"Missing translation at {pointer}: '{value}'")
                missing_translations += 1

        print(f"\nTotal Messages: {len(translatable_items)}")

        if missing_translations:
            print(f"Total Missing: {missing_translations}")

        return SurveySchema(translated_schema)
