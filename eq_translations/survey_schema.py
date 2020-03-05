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
    keys_for_translation = [
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
    def pointer_dicts(self):
        pointers = []

        for key in self.keys_for_translation:
            with_context = key in self.keys_with_context

            for pointer in find_pointers_to(self.schema, key):
                # The 'list' property is used by both 'contents' and 'when' blocks.
                if "/when/" in pointer:
                    continue

                schema_element = resolve_pointer(self.schema, pointer)
                if isinstance(schema_element, dict):
                    pointers_found = self._get_pointers_from_dict_element(
                        schema_element, pointer, with_context
                    )
                    pointers.extend(pointers_found)

                elif isinstance(schema_element, list):
                    pointers_found = self._get_pointers_from_list_element(
                        schema_element, pointer, with_context
                    )
                    pointers.extend(pointers_found)

                else:
                    pointer_dict = self._get_pointer_dict(pointer, with_context)
                    pointers.append(pointer_dict)

        return pointers

    def _get_pointers_from_list_element(self, schema_element, pointer, with_context):
        pointers = []
        for idx, _ in enumerate(schema_element):
            sub_element = schema_element[idx]
            if isinstance(sub_element, str):
                new_pointer = f"{pointer}/{idx}"
                pointer_dict = self._get_pointer_dict(new_pointer, with_context)
                pointers.append(pointer_dict)

        return pointers

    def _get_pointers_from_dict_element(self, schema_element, pointer, with_context):
        pointers = []
        if "text_plural" in schema_element:
            new_pointer = f"{pointer}/text_plural"
            pointer_dict = self._get_pointer_dict(new_pointer, with_context)
            pointers.append(pointer_dict)
            return pointers

        for element in schema_element:
            sub_element = schema_element[element]
            if isinstance(sub_element, str):
                new_pointer = f"{pointer}/{element}"
                pointer_dict = self._get_pointer_dict(new_pointer, with_context)
                pointers.append(pointer_dict)

        return pointers

    def _get_pointer_dict(self, pointer, with_context):
        pointer_dict = {"pointer": pointer}

        if with_context and f"/answers/" in pointer:
            message_context = self._get_message_context_from_pointer(pointer)
            pointer_dict["context"] = message_context

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

    def _get_message_context_from_pointer(self, pointer):
        question = self.get_parent_question(pointer)

        if "text_plural" in question:
            message_context = question["text_plural"]["forms"]["other"]
        elif "placeholders" in question:
            message_context = question["text"]
        else:
            message_context = question

        return f"Answer for: {message_context}"

    @property
    def catalog(self):
        """
        :return: a schema catalog to be used as the content within a po/pot file
        """
        catalog = Catalog()

        for pointer_dict in self.pointer_dicts:
            message_context = pointer_dict.get("context")
            pointer_contents = resolve_pointer(self.schema, pointer_dict["pointer"])

            if not pointer_contents:
                continue

            message_id = get_message_id(content=pointer_contents)
            catalog.add(
                id=message_id, context=message_context,
            )

        print(f"Total Messages: {len(self.pointer_dicts)}")

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

        for pointer_dict in self.pointer_dicts:
            pointer = pointer_dict["pointer"]
            pointer_contents = resolve_pointer(self.schema, pointer)

            if not pointer_contents:
                continue

            message_id = get_message_id(pointer_contents)
            message_context = pointer_dict.get("context")

            translation = schema_translation.get_translation(
                message_id, message_context
            )

            if translation:
                if isinstance(translation, tuple) and language_code:
                    plural_forms = get_plural_forms_for_language(language_code)
                    for idx, plural in enumerate(plural_forms):
                        plural_form_pointer = f"{pointer}/forms/{plural}"
                        set_pointer(
                            translated_schema,
                            plural_form_pointer,
                            dumb_to_smart_quotes(translation[idx]),
                        )
                else:
                    set_pointer(
                        translated_schema, pointer, dumb_to_smart_quotes(translation),
                    )
            else:
                print(f"Missing translation at {pointer}: '{pointer_contents}'")
                missing_translations += 1

        print(f"\nTotal Messages: {len(self.pointer_dicts)}")

        if missing_translations:
            print(f"Total Missing: {missing_translations}")

        return SurveySchema(translated_schema)
