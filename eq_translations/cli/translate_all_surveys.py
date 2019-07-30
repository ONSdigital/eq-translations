import argparse
import os

from eq_translations.survey_schema import SurveySchema
from eq_translations.schema_translation import SchemaTranslation

def main():
    parser = argparse.ArgumentParser(description='Translate all surveys in a directory')

    parser.add_argument(
        'SCHEMA_DIRECTORY_PATH',
        help='The path to the source schema to be translated'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.SCHEMA_DIRECTORY_PATH):
        print('Schema directory does not exist')
        exit(2)

    available_translations = os.listdir('./translations')

    for translation_filename in available_translations:
        if not translation_filename.endswith('.po'):
            continue

        translation_name = translation_filename.strip('.po')
        schema_name, target_language = translation_name.split('_translate_')
        schema_filename = '{}.json'.format(schema_name)
        schema_path = os.path.join(args.SCHEMA_DIRECTORY_PATH, 'en', schema_filename)

        if os.path.exists(schema_path):
            print('Translating schema: {schema_path}\n')
            schema = SurveySchema()
            schema.load(schema_path)

            translation = SchemaTranslation()
            translation.load('./translations/{translation_filename}')

            target_dir_path = os.path.join(args.SCHEMA_DIRECTORY_PATH, target_language)

            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)

            target_path = os.path.join(target_dir_path, schema_filename)
            translated_schema = schema.translate(translation)
            translated_schema.save(target_path)
            print('Created schema: {target_path}\n')


if __name__ == '__main__':
    main()
