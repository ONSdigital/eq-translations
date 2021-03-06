from jsonpointer import resolve_pointer
from termcolor import colored

from eq_translations.utils import (
    list_pointers,
    find_pointers_to,
    get_plural_forms_for_language,
)


def get_missing_non_plural_pointers(source_schema, target_schema):
    """
    Compare the pointers in two json structures and return differences
    :param source_schema: Structure to identify differences against
    :param target_schema: Target structure to compare against
    :return:
    """
    non_plural_source_survey_pointers = {
        p for p in list_pointers(source_schema) if "text_plural" not in p
    }
    non_plural_target_survey_pointers = {
        p for p in list_pointers(target_schema) if "text_plural" not in p
    }

    missing_target_pointers = non_plural_source_survey_pointers.difference(
        non_plural_target_survey_pointers
    )
    missing_source_pointers = non_plural_target_survey_pointers.difference(
        non_plural_source_survey_pointers
    )

    missing_pointers = missing_target_pointers | missing_source_pointers

    if missing_pointers:
        print(
            colored(
                f"\nDifferences between source/target schema strings (excluding text_plural): {len(missing_pointers)}",
                "red",
            )
        )
        print(
            f"Total non-plural strings in source schema: {len(non_plural_source_survey_pointers)}"
        )
        print(
            f"Total non-plural strings in target schema: {len(non_plural_target_survey_pointers)}"
        )

        if missing_source_pointers:
            print("Missing from the source schema:")
            for pointer in missing_source_pointers:
                print(colored(f"  - {pointer}", "yellow"))

        if missing_target_pointers:
            print("Missing from the target schema:")
            for pointer in missing_target_pointers:
                print(colored(f"  - {pointer}", "yellow"))

    return missing_pointers


def get_missing_translated_plural_forms(translated_schema, language):
    missing_plural_forms = []
    plural_forms = get_plural_forms_for_language(language)
    plural_pointers = find_pointers_to(translated_schema, "text_plural")

    for pointer in plural_pointers:
        text_plural_forms = resolve_pointer(translated_schema, pointer)["forms"]
        for form in plural_forms:
            if not text_plural_forms.get(form):
                missing_plural_forms.append((pointer, form))

    if missing_plural_forms:
        print(
            colored(
                f"\nTotal plural forms missing in translated schema: {len(missing_plural_forms)}",
                "red",
            )
        )
        print("Missing plural forms at:")

        for pointer, form in missing_plural_forms:
            print(colored(f"  - {pointer}/forms/: '{form}'", "yellow"))

    return missing_plural_forms
