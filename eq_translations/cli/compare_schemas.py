import argparse
import os

from eq_translations.utils import compare_schemas
from eq_translations.survey_schema import SurveySchema

def main():
    parser = argparse.ArgumentParser(description='Compare two schemas for structure differences')

    parser.add_argument(
        'SOURCE_SCHEMA',
        help='The path to the source schema'
    )

    parser.add_argument(
        'TARGET_SCHEMA',
        help='The path to the target schema to compare against'
    )

    args = parser.parse_args()

    if not os.path.exists(args.SOURCE_SCHEMA):
        print(f'{args.SOURCE_SCHEMA} does not exist')
        exit(2)
    if not os.path.exists(args.TARGET_SCHEMA):
        print(f'{args.TARGET_SCHEMA} does not exist')
        exit(2)

    source_survey = SurveySchema()
    source_survey.load(args.SOURCE_SCHEMA)
    target_survey = SurveySchema()
    target_survey.load(args.TARGET_SCHEMA)

    compare_schemas(source_survey.schema, target_survey.schema)


if __name__ == '__main__':
    main()
