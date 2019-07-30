import argparse
import os

from eq_translations.entrypoints import handle_compare_schemas

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

    handle_compare_schemas(args.SOURCE_SCHEMA, args.TARGET_SCHEMA)


if __name__ == '__main__':
    main()
