from jsonpointer import resolve_pointer

from eq_translations import SurveySchema
from eq_translations.utils import list_pointers, get_plural_forms_for_language


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

    missing_pointers = {
        pointer
        for pointer in (missing_target_pointers | missing_source_pointers)
        if "text_plural" not in pointer
    }

    for pointer in missing_pointers:
        print(f"Missing Pointer: {pointer}")

    print(f"Total attributes in source schema: {len(source_survey_pointers)}")
    print(f"Total attributes in target schema: {len(target_survey_pointers)}")
    print(
        f"Differences between source/target schema attributes (excluding text_plural): {len(missing_pointers)}\n"
    )

    return missing_pointers


def validate_translated_plural_forms(translated_schema, language_code):
    context_plural_pointers, no_context_plural_pointers = SurveySchema(
        translated_schema
    ).get_plural_pointers()

    plurals_for_language = get_plural_forms_for_language(language_code)

    missing_plural_forms = []
    for pointer in context_plural_pointers + no_context_plural_pointers:
        text_plural_forms = resolve_pointer(translated_schema, pointer)["forms"]

        for form in plurals_for_language:
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
