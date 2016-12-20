# eq-translations
Scripts for translating eq-survey-runner surveys

## Setup
Based on python 3

If using virtualenvwrapper (if not, you should be), create a new virtual env for python3

```
mkvirtual --python=`which python3` <your env name>
```

Install dependencies using pip

```
pip install -r requirements.txt
```

## Usage 
Extract translatable text from an eQ survey with

```
./scripts/run_translation_extract.sh <json_file> [output_directory]
```
This will output the translatable text to an Excel (.xlsx) file. 

After the text has been translated, create a new translated survey with
```
./scripts/run_translate_survey.sh <json_file> <translations_file> [output_directory]
