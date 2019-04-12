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

To run the tests:

```
make test
```

## Naming conventions

### Translation files

Should be prefixed with the name of the schema to translate followed by `_translate_` followed by the [country code](https://en.wikipedia.org/wiki/ISO_3166-1) of the translations in a po format e.g.

```
census_household_translate_cy.po