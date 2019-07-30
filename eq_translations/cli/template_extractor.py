import argparse
import os

from eq_translations.entrypoints import extract_template

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


if __name__ == '__main__':
    main()
