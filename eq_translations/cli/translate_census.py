import os
import sys
import argparse

import requests
from tqdm import tqdm

from eq_translations.survey_schema import SurveySchema
from eq_translations.schema_translation import SchemaTranslation

project_id = "eq-census"


def main():
    try:
        os.environ["CROWDIN_PROJECT_API_KEY"]
    except KeyError:
        print("Required environment variable is not set: CROWDIN_PROJECT_API_KEY")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Translate the census survey using crowdin"
    )

    parser.add_argument(
        "SCHEMA_PATH", help="The path to the source schema to be translated"
    )

    parser.add_argument(
        "OUTPUT_DIRECTORY",
        help="The destination directory for the translation template",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print("Output directory does not exist")
        exit(1)

    file_prefix = "individual" if "individual" in args.SCHEMA_PATH else "household"
    template_file = f"census_{file_prefix}.pot"
    output_file = f"census_{file_prefix}-cy.po"

    download_url = "https://api.crowdin.com/api/project/{project_id}/export-file?key={project_api_key}&file={file}&language={language}".format(
        project_id=project_id,
        project_api_key=os.getenv("CROWDIN_PROJECT_API_KEY"),
        file=template_file,
        language="cy",
    )

    print("Fetching translation file from crowdin")

    response = requests.get(download_url, stream=True)

    if not response:
        print("Empty response from crowdin")
        exit(1)

    output_path = os.path.join(args.OUTPUT_DIRECTORY, output_file)

    with open(output_path, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    schema = SurveySchema()
    schema.load(args.SCHEMA_PATH)
    schema_name = os.path.basename(args.SCHEMA_PATH)

    translation = SchemaTranslation()
    translation.load(output_path)

    translated_schema = schema.translate(translation)
    translated_schema.save(os.path.join(args.OUTPUT_DIRECTORY, schema_name))


if __name__ == "__main__":
    main()
