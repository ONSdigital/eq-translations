import argparse
import os
import subprocess

from app.survey_schema import SurveySchema
from app.schema_translation import SchemaTranslation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract a combined translation template from census json schemas")

    parser.add_argument(
        'RUNNER_SCHEMA_DIRECTORY',
        help="The path to the runner directory from which data will be extracted"
    )

    parser.add_argument(
        'OUTPUT_DIRECTORY',
        help="The destination directory for the translation template"
    )

    args = parser.parse_args()

    if not os.path.isdir(os.path.join(args.RUNNER_SCHEMA_DIRECTORY)):
        print("Runner schema directory does not exist")

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print("Output directory does not exist")

    census_schemas = ['census_individual_gb_eng.json', 'census_individual_gb_wls.json']
    translation_names = []

    for census_schema in census_schemas:
        print(f"Extracting from: {census_schema}")
        survey = SurveySchema()
        survey.load(os.path.join(args.RUNNER_SCHEMA_DIRECTORY, census_schema))

        catalog = survey.get_catalog()

        schema_name, _ = os.path.splitext(census_schema)

        translation_name = f"{schema_name}.pot"
        translation = SchemaTranslation(catalog)
        translation.save(os.path.join(args.OUTPUT_DIRECTORY, translation_name))
        translation_names.append(translation_name)

    print("Concatenating census extractions together")

    subprocess.run(['msgcat'] + translation_names + ['-o', 'census_individual.pot'], cwd=args.OUTPUT_DIRECTORY)
