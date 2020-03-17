from jsonpointer import resolve_pointer

from eq_translations.utils import (
    list_pointers,
    find_pointers_to,
)


def compare_schemas(source_schema, target_schema):
    """
    Compare the pointers in two json structures and return differences
    :param source_schema: Structure to identify differences against
    :param target_schema: Target structure to compare against
    :return:
    """
    source_survey_pointers = set(list_pointers(source_schema))
    target_survey_pointers = set(list_pointers(target_schema))

    missing_target_pointers = source_survey_pointers.difference(target_survey_pointers)
    missing_source_pointers = target_survey_pointers.difference(source_survey_pointers)

    missing_non_plural_target_pointers = {
        pointer for pointer in missing_target_pointers if "text_plural" not in pointer
    }
    missing_non_plural_source_pointers = {
        pointer for pointer in missing_source_pointers if "text_plural" not in pointer
    }

    missing_pointers = (
        missing_non_plural_target_pointers | missing_non_plural_source_pointers
    )

    if missing_pointers:
        print(
            f"\nDifferences between source/target schema strings (excluding text_plural): {len(missing_pointers)}"
        )
        print(f"Total strings in source schema: {len(source_survey_pointers)}")
        print(f"Total strings in target schema: {len(target_survey_pointers)}\n")

        if missing_target_pointers:
            print(
                "Pointers in the source schema that are missing from the target schema:"
            )
            for pointer in missing_target_pointers:
                print(pointer)

        if missing_source_pointers:
            print(
                "Pointers in the target schema that are missing from the source schema:"
            )
            for pointer in missing_source_pointers:
                print(pointer)

    return missing_pointers


def validate_translated_plural_forms(translated_schema, plural_forms):
    missing_plural_forms = []
    plural_pointers = find_pointers_to(translated_schema, "text_plural")

    for pointer in plural_pointers:
        text_plural_forms = resolve_pointer(translated_schema, pointer)["forms"]

        for form in plural_forms:
            if not text_plural_forms.get(form):
                missing_plural_forms.append(form)
                print(
                    f"Missing plural form in translated schema at {pointer}/forms/: '{form}'"
                )

    if missing_plural_forms:
        print(
            f"\nTotal plural forms missing in translated schema: {len(missing_plural_forms)}"
        )

    return missing_plural_forms
