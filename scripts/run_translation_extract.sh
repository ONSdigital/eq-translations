#!/bin/bash

if [ "$#" -gt 2 -o "$#" -lt 1 ]; then
    echo ""
    echo "Usage: $0 <json_file> [output_directory]"
    echo ""
    exit 1
fi

JSON_FILE=$1

if [ -z $2 ]; then
    # Use current working directory
    OUTPUT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    # Use the directory passed in
    OUTPUT_DIR=$2
fi


if [ ! -f ${JSON_FILE} ]; then
    echo "JSON file '${JSON_FILE}' does not exist!"
    exit 2
fi

if [ ! -d ${OUTPUT_DIR} ]; then
    echo "Directory '${OUTPUT_DIR}' does not exist!"
    exit 2
fi

python ./translations/extract_translation_data.py ${JSON_FILE} ${OUTPUT_DIR}
