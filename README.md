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
pipenv run ./scripts/run_translation_extract.sh <json_file> [output_directory]
```
This will output the translatable text to an Excel (.xlsx) file.

After the text has been translated, create a new translated survey with
```
pipenv run ./scripts/run_translate_survey.sh <json_file> <translations_file> [output_directory]
```

To translate all surveys in a directory run

```
pipenv run ./scripts/run_translate_all_surveys <top_level_directory_containing_schemas>
```

## Naming conventions

### Translation files

Should be prefixed with the name of the schema to translate followed by `_translate_` followed by the [country code](https://en.wikipedia.org/wiki/ISO_3166-1) of the translations in a xlsx format e.g.

```
census_household_translate_cy.xlsx
```