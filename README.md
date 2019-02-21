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
pipenv run python -m app.template_extractor <schema_file> <output_directory>
```
This will output the translatable text to an POT file.