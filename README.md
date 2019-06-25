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

## Usage
Extract translatable text from an eQ survey with

```
pipenv run python -m cli.template_extractor <schema_file> <output_directory>
```
This will output the translatable text to an POT file.


After the text has been translated, create a new translated survey with:

```
pipenv run python -m cli.translate_survey <schema_file> <translation_path> <output_directory>
```

To translate all surveys in a directory run:

```
pipenv run python -m cli.translate_all_surveys <top_level_schema_directory>
```

To compare two schemas for differences in structure:

```
pipenv run python -m cli.compare_schemas <path_to_source_schema> <path_to_target_schema>
```

To run the tests:

```
make test
```

### Census Commands

To extract the census individual schema from Survey Runner to a pot template

```
pipenv run python -m cli.extract_census_template <runner_schema_directory> <output_directory>
pipenv run python -m cli.extract_census_template ../eq-survey-runner/data/en out
```

To translate the census individual using current translations in crowdin

```
pipenv run python -m cli.extract_census_template <census_schema> <output_directory>
pipenv run python -m cli.translate_census ../eq-survey-runner/data/en/census_individual_gb_eng.json out
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