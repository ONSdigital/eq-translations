# eq-translations

Scripts for translating eq-survey-runner surveys

## Setup

Upgrade pip and install dependencies:

```
brew install pyenv
pyenv install
pip install --upgrade pip setuptools pipenv
pipenv install --dev
```

## Python Package Usage

`eq_translations` is packaged as a python package, though it is not currently published on pypi. 

To install, replace `BRANCHNAME` with an appropriate tag or branch (or master) and run#:

```
pipenv install -e git+https://github.com/ONSDigital/eq-translations.git@BRANCHNAME#egg=eq_translations
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

The following scripts will also be available on your path once the package is installed: `template_extractor`, `translate_census`, `translate_survey`, `compare_schemas`

## Usage without library

To use this package without installing it as a python package, the following commands can be run: 

Extract translatable text from an eQ survey with

```
pipenv run python -m eq_translations.cli.template_extractor <schema_file> <output_directory>
```
This will output the translatable text to an POT file.


After the text has been translated, create a new translated survey with:

```
pipenv run python -m eq_translations.cli.translate_survey <schema_file> <translation_path> <output_directory>
```

To compare two schemas for differences in structure:

```
pipenv run python -m eq_translations.cli.compare_schemas <path_to_source_schema> <path_to_target_schema>
```

To run the tests:

```
make test
```

### Census Commands

To translate the census individual using current translations in crowdin

```
pipenv run python -m eq_translations.cli.extract_census_template <census_schema> <output_directory>
pipenv run python -m eq_translations.cli.translate_census ../eq-survey-runner/data/en/census_individual_gb_eng.json out
```

## Naming conventions

### Translation files

Should be prefixed with the name of the schema to translate followed by `_translate_` followed by the [country code](https://en.wikipedia.org/wiki/ISO_3166-1) of the translations in a po format e.g.

```
census_household_translate_cy.po
```

## Managing translations

When `gettext` is installed there are a number of command line utilities that can help with managing translations.

To merge the translations from an already translated survey into another one, you can use `msgmerge`. For example `msgmerge census_household-cy.po census_individual.pot -o census_individual-cy.po` will merge matching Welsh translations from the Census household questionnaire into the Census individual questionnaire.

To add the content of translation files together, you can use `msgcat`. For example `msgcat census_individual-wls.pot census_individual-gb.pot -o census_individual.pot` will add unique messages from each input template file to create an output Census individual template for both versions.