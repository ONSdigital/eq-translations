import argparse
import os

from app.survey_schema import SurveySchema
from app.schema_translation import SchemaTranslation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Translate a survey using a po file")

    parser.add_argument(
        'SCHEMA_PATH',
        help="The path to the source schema to be translated"
    )
    parser.add_argument(
        'TRANSLATION_PATH',
        help="The path to the source po file containing translations"
    )

    parser.add_argument(
        'OUTPUT_DIRECTORY',
        help="The destination directory for the translation template"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print("Not a valid output directory")
        exit(2)

    schema = SurveySchema()
    schema.load(args.SCHEMA_PATH)

    schema_name = os.path.basename(args.SCHEMA_PATH)

    translation = SchemaTranslation()
    translation.load(args.TRANSLATION_PATH)

    translated_schema = schema.translate(translation)
    translated_schema.save(os.path.join(args.OUTPUT_DIRECTORY, schema_name))
