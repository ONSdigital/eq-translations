import argparse
import os

from eq_translations.utils import compare_schemas
from eq_translations.survey_schema import SurveySchema
from eq_translations.schema_translation import SchemaTranslation

def main():
    parser = argparse.ArgumentParser(description='Translate a survey using a po file')

    parser.add_argument(
        'SCHEMA_PATH',
        help='The path to the source schema to be translated'
    )
    parser.add_argument(
        'TRANSLATION_PATH',
        help='The path to the source po file containing translations'
    )

    parser.add_argument(
        'OUTPUT_DIRECTORY',
        help='The destination directory for the translation template'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print('Not a valid output directory')
        exit(2)

    translate_schema(args.SCHEMA_PATH, args.TRANSLATION_PATH, args.OUTPUT_DIRECTORY)

def translate_schema(schema_path, translation_path, output_directory):
    survey_schema = SurveySchema()
    survey_schema.load(schema_path)

    schema_name = os.path.basename(schema_path)

    translation = SchemaTranslation()
    translation.load(translation_path)

    translated_schema = survey_schema.translate(translation)
    translated_schema.save(os.path.join(output_directory, schema_name))

    compare_schemas(survey_schema.schema, translated_schema.schema)

if __name__ == '__main__':
    main()
