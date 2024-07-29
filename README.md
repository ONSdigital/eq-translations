# eq-translations

Scripts for translating eq-survey-runner schemas 

## Setup

It is recommended to use [Pyenv](https://github.com/pyenv/pyenv-installer) via Git

Upgrade pip and install dependencies:
```
curl https://pyenv.run | bash
exec $SHELL
pyenv install
pip install --upgrade pip setuptools
```

## Install poetry, poetry dotenv plugin and install dependencies:

``` shell
curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2
poetry self add poetry-plugin-dotenv
poetry install
```

We use [poetry-plugin-up](https://github.com/MousaZeidBaker/poetry-plugin-up) to update dependencies in the `pyproject.toml` file:

```shell
poetry self add poetry-plugin-up
```

## Python Package Usage

`eq_translations` is packaged as a python package, though it is not currently published on pypi.

To install, replace `BRANCHNAME` with an appropriate tag or branch and run:

```
poetry install -e git+https://github.com/ONSDigital/eq-translations.git@BRANCHNAME#egg=eq_translations
```

You can also install it locally running the following from the root directory:

```
pip install .
```

### Basic library Usage
The library exports a `eq_translations.SurveySchema` class and `eq_translations.SchemaTranslation` class. These classes can be used directly to perform translations, or there are some helper methods available in `eq_translations.entrypoints`:

`extract_template(schema_path, output_directory)`

`translate_schema(schema_path, translation_path, output_directory)`

`handle_compare_schemas(source_schema, target_schema)`

The following scripts will also be available on your path once the package is installed: `extract_template`, `translate_schema`, `compare_schemas`

## Usage without library

To use this package without installing it as a python package, the following commands can be run: 

Extract translatable text from an eQ schema with

```
poetry run python -m eq_translations.cli.extract_template <schema_file> <output_directory>
```
This will output the translatable text to an POT file.


After the text has been translated, create a new translated schema with:

```
poetry run python -m eq_translations.cli.translate_schema <schema_file> <translation_path> <output_directory>
```

To compare two schemas for differences in structure:

```
poetry run python -m eq_translations.cli.compare_schemas <path_to_source_schema> <path_to_target_schema>
```

To run the tests:

```
make test
```

## Naming conventions

### Translation files

Should be prefixed with the name of the schema to translate followed by `_translate_` followed by the [country code](https://en.wikipedia.org/wiki/ISO_3166-1) of the translations in a po format e.g.

```
<schema_name>_translate_cy.po
```

## Managing translations

When `gettext` is installed there are a number of command line utilities that can help with managing translations.

To merge the translations from an already translated schema into another one, you can use `msgmerge`. For example `msgmerge <translated_schema>-cy.po <target_schema>.pot -o <target_schema>-cy.po` will merge matching Welsh translations from the translated schema into the not yet translated target schema.

To add the content of translation files together, you can use `msgcat`. For example `msgcat <schema_name>.pot <schema_name>-gb.pot -o <schema_name>.pot` will add unique messages from each input template file to create an output template for both schema versions.
