import argparse
import os

from app.survey_schema import SurveySchema
from app.schema_translation import SchemaTranslation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract translation template from json schema")

    parser.add_argument(
        'SCHEMA_PATH',
        help="The path to the source schema from which data will be extracted"
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
    catalog = schema.get_catalog()

    schema_name, _ = os.path.splitext(os.path.basename(args.SCHEMA_PATH))

    translation = SchemaTranslation(catalog)
    translation.save(os.path.join(args.OUTPUT_DIRECTORY, "{}.pot".format(schema_name)))
