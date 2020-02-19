import os

from eq_translations import SurveySchema, SchemaTranslation
from eq_translations.validate_translation import (
    compare_schemas,
    validate_translated_plural_forms,
)


def handle_extract_template(schema_path, output_directory):
    schema = SurveySchema()
    schema.load(schema_path)
    catalog = schema.get_catalog

    schema_name, _ = os.path.splitext(os.path.basename(schema_path))

    translation = SchemaTranslation(catalog)
    translation.save(os.path.join(output_directory, "{}.pot".format(schema_name)))


def handle_translate_schema(
    schema_path, translation_path, output_directory, target_language_code
):
    survey_schema = SurveySchema()
    survey_schema.load(schema_path)

    schema_name = os.path.basename(schema_path)

    translation = SchemaTranslation()
    translation.load(translation_path)

    translated_schema = survey_schema.translate(translation, target_language_code)
    translated_schema.save(os.path.join(output_directory, schema_name))

    compare_schemas(survey_schema.schema, translated_schema.schema)

    validate_translated_plural_forms(translated_schema.schema, target_language_code)


def handle_compare_schemas(source_schema, target_schema, target_language_code):
    source_survey = SurveySchema()
    source_survey.load(source_schema)
    target_survey = SurveySchema()
    target_survey.load(target_schema)

    compare_schemas(source_survey.schema, target_survey.schema)

    validate_translated_plural_forms(target_schema.schema, target_language_code)
