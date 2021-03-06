import argparse
import os
import sys

from eq_translations.entrypoints import handle_translate_schema


def main():
    parser = argparse.ArgumentParser(description="Translate a schema using a po file")

    parser.add_argument(
        "SCHEMA_PATH", help="The path to the source schema to be translated"
    )
    parser.add_argument(
        "TRANSLATION_PATH",
        help="The path to the source po file containing translations",
    )

    parser.add_argument(
        "OUTPUT_DIRECTORY",
        help="The destination directory for the translation template",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.OUTPUT_DIRECTORY):
        print("Not a valid output directory")
        sys.exit(2)

    handle_translate_schema(
        args.SCHEMA_PATH, args.TRANSLATION_PATH, args.OUTPUT_DIRECTORY
    )


if __name__ == "__main__":
    main()
