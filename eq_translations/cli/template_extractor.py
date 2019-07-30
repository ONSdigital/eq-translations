import argparse
import os

from eq_translations.survey_schema import SurveySchema
from eq_translations.schema_translation import SchemaTranslation

def main():
    parser = argparse.ArgumentParser(description='Extract translation template from json schema')

    parser.add_argument(
        'SCHEMA_PATH',
        help='The path to the source schema from which data will be extracted'
    )

    parser.add_argument(
        'OUTPUT_DIRECTORY',
        help='The destination directory for the translation template'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print('Output directory does not exist')
        exit(2)

    extract_template(args.SCHEMA_PATH, args.OUTPUT_DIRECTORY)

def extract_template(schema_path, output_directory):

    schema = SurveySchema()
    schema.load(schema_path)
    catalog = schema.get_catalog()

    schema_name, _ = os.path.splitext(os.path.basename(schema_path))

    translation = SchemaTranslation(catalog)
    translation.save(os.path.join(output_directory, '{}.pot'.format(schema_name)))


if __name__ == '__main__':
    main()
