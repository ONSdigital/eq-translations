#!/bin/bash

function parent_directory {
    current_dir=$(dirname "$1")
    parent_dir="$( cd "${current_dir}" && pwd )"
    echo $parent_dir
}

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

current_dir_path=$(parent_directory "${BASH_SOURCE[0]}")
parent_dir_path=$(parent_directory "${current_dir_path}")
python "${parent_dir_path}"/app/translate_survey.py ${JSON_FILE} ${TRANSLATIONS_FILE} ${OUTPUT_DIR}
