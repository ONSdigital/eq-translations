import os

from termcolor import colored

from eq_translations import SurveySchema, SchemaTranslation
from eq_translations.validate_translation import (
    compare_schemas,
    validate_translated_plural_forms,
)


def handle_extract_template(schema_path, output_directory):
    schema = SurveySchema()
    schema.load(schema_path)

    schema_name, _ = os.path.splitext(os.path.basename(schema_path))

    translation = SchemaTranslation(schema.catalog)
    translation.save(os.path.join(output_directory, f"{schema_name}.pot"))


def handle_translate_schema(schema_path, translation_path, output_directory):
    survey_schema = SurveySchema()
    survey_schema.load(schema_path)

    schema_name = os.path.basename(schema_path)

    translation = SchemaTranslation()
    translation.load(translation_path)

    translated_schema = survey_schema.translate(translation)
    translated_schema.save(os.path.join(output_directory, schema_name))

    missing_pointers = compare_schemas(survey_schema.schema, translated_schema.schema)

    missing_plural_forms = validate_translated_plural_forms(
        translated_schema.schema, translated_schema.language
    )

    if not (missing_pointers and missing_plural_forms):
        print(colored("\nSchema Translated Successfully", "green"))


def handle_compare_schemas(source_schema, target_schema):
    source_survey = SurveySchema()
    source_survey.load(source_schema)
    target_survey = SurveySchema()
    target_survey.load(target_schema)

    missing_pointers = compare_schemas(source_survey.schema, target_survey.schema)

    missing_plural_forms = validate_translated_plural_forms(
        target_survey.schema, target_survey.language
    )

    if not (missing_pointers and missing_plural_forms):
        print(
            colored("\nNo Structural Difference Between Source/Target Schema", "green")
        )
