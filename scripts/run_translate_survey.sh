#!/bin/bash

if [ "$#" -gt 3 -o "$#" -lt 1 ]; then
    echo ""
    echo "Usage: $0 <json_file> <translations_file> [output_directory]"
    echo ""
    exit 1
fi

JSON_FILE=$1
TRANSLATIONS_FILE=$2

if [ -z $3 ]; then
    # Use current working directory
    OUTPUT_DIR=$PWD
else
    # Use the directory passed in
    OUTPUT_DIR=$3
fi


if [ ! -f ${JSON_FILE} ]; then
    echo "JSON file '${JSON_FILE}' does not exist!"
    exit 2
fi

if [ ! -f ${TRANSLATIONS_FILE} ]; then
    echo "Translations file '${TRANSLATIONS_FILE}' does not exist!"
    exit 2
fi

if [ ! -d ${OUTPUT_DIR} ]; then
    echo "Directory '${OUTPUT_DIR}' does not exist!"
    exit 2
fi

python ./translations/translate_survey.py ${JSON_FILE} ${TRANSLATIONS_FILE} ${OUTPUT_DIR}
