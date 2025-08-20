import copy
import json

from babel.messages import Catalog
from jsonpath_ng import parse
from jsonpointer import set_pointer
from termcolor import colored

from eq_translations.extractable_strings import EXTRACTABLE_STRINGS, CONTEXT_DEFINITIONS
from eq_translations.translatable_item import TranslatableItem
from eq_translations.utils import (
    json_path_to_json_pointer,
    get_message_id,
    dumb_to_smart_quotes,
    get_plural_forms_for_language,
    get_parent_schema_object,
)


class SurveySchema:
    schema = {}

    def __init__(self, schema_data=None):
        self.schema = schema_data

    def load(self, schema_path):
        with open(schema_path, encoding="utf8") as schema_file:  # pragma: no cover
            self.schema = json.load(schema_file)  # pragma: no cover

    def save(self, schema_path):
        with open(schema_path, "w", encoding="utf8") as schema_file:  # pragma: no cover
            return json.dump(self.schema, schema_file, indent=4)  # pragma: no cover

    @property
    def language(self):
        return self.schema.get("language")

    @property
    def translatable_items(self):
        """
        :yield: A TranslatableItem
        :return: A generator
        """
        for extractable_string in EXTRACTABLE_STRINGS:
            json_path = parse(extractable_string["json_path"])

            for match in json_path.find(self.schema):
                json_pointer, string_value = self._get_json_pointer_and_string_value(
                    str(match.full_path), match.value
                )
                additional_context = []
                for context_type in extractable_string.get("additional_context", []):
                    context = self._get_context_for_pointer(json_pointer, context_type)
                    if context:
                        additional_context.append(context)

                yield TranslatableItem(
                    pointer=json_pointer,
                    description=extractable_string["description"],
                    value=string_value,
                    context=self._get_context_for_pointer(
                        json_pointer, extractable_string.get("context")
                    ),
                    additional_context=additional_context or None,
                )

    @staticmethod
    def _get_json_pointer_and_string_value(json_path, schema_object):
        """
        Resolves the given schema_object to a json pointer and value
        :return: json pointer, string value
        """
        json_pointer = json_path_to_json_pointer(json_path)
        if isinstance(schema_object, dict):
            plural_forms = schema_object.get("text_plural", {}).get("forms")
            if plural_forms:
                return f"{json_pointer}/text_plural/forms", plural_forms
            return f"{json_pointer}/text", schema_object["text"]

        return json_pointer, schema_object

    @staticmethod
    def _get_single_string_value(schema_object):
        """
        Resolves an identifying string value for the schema_object. If plural the `other` form is returned.
        :return: string value
        """
        if isinstance(schema_object, dict):
            if "text_plural" in schema_object:
                return schema_object["text_plural"]["forms"]["other"]
            return schema_object["text"]
        return schema_object

    def _get_context_for_pointer(self, pointer, context_type):
        context_definition = CONTEXT_DEFINITIONS.get(context_type)
        if context_definition:
            parent_schema_object = get_parent_schema_object(
                self.schema, pointer, context_definition["parent_schema_property"]
            )
            if context_definition["property"] in parent_schema_object:
                context_string = self._get_single_string_value(
                    parent_schema_object[context_definition["property"]]
                )
                return context_definition["text"].format(context=context_string)

    @property
    def catalog(self):
        """
        :return: a schema catalog to be used as the content within a po/pot file
        """
        catalog = Catalog()

        translatable_items = list(self.translatable_items)

        for translatable_item in translatable_items:
            if not translatable_item.value:
                continue

            message_id = get_message_id(translatable_item.value)
            auto_comments = [translatable_item.description]
            if translatable_item.additional_context:
                auto_comments += translatable_item.additional_context
            catalog.add(
                id=message_id,
                context=translatable_item.context,
                auto_comments=auto_comments,
            )

        print(f"Total Translatable Items: {len(translatable_items)}")

        return catalog

    def translate(self, schema_translation):
        """
        Use the supplied schema translation object to translate all translatable strings
        within the survey

        :param schema_translation: The SchemaTranslation object
        :return:
        """
        translated_schema = copy.deepcopy(self.schema)
        translated_schema["language"] = schema_translation.language

        missing_translations = 0
        translatable_items = list(self.translatable_items)

        for translatable_item in translatable_items:
            if not translatable_item.value:
                continue

            message_id = get_message_id(translatable_item.value)
            context = translatable_item.context

            translation = schema_translation.get_translation(message_id, context)

            if translation:
                if isinstance(translation, tuple):
                    plural_forms = get_plural_forms_for_language(
                        schema_translation.language
                    )
                    for index, plural_form in enumerate(plural_forms):
                        plural_form_pointer = (
                            f"{translatable_item.pointer}/{plural_form}"
                        )
                        set_pointer(
                            translated_schema,
                            plural_form_pointer,
                            dumb_to_smart_quotes(translation[index]),
                        )
                else:
                    set_pointer(
                        translated_schema,
                        translatable_item.pointer,
                        dumb_to_smart_quotes(translation),
                    )
            else:
                missing_translations += 1

                if missing_translations == 1:
                    print("Missing translation at:")

                print(
                    colored(
                        f"  - {translatable_item.pointer}: '{translatable_item.value}'",
                        "yellow",
                    )
                )

        print(f"\nTotal Translatable Items: {len(translatable_items)}")

        if missing_translations:
            print(
                colored(f"Total Missing Translations: {missing_translations}", "yellow")
            )

        return SurveySchema(translated_schema)
