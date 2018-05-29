#!/usr/bin/env bash

function parent_directory {
  current_dir=$(dirname "$1")
  parent_dir="$( cd "${current_dir}" && pwd )"
  echo "${parent_dir}"
}

function translate_all_schemas {
  while read -r filename
    do
      filename_regex="([a-zA-Z_]+)_translate_([a-zA-Z]{2}).xlsx"
      if [[ $filename =~ $filename_regex ]]; then
        schema=${BASH_REMATCH[1]};
        country_code=${BASH_REMATCH[2]};
        mkdir -p "${path_to_schemas}"/"${country_code}"
        "${parent_dir_path}"/scripts/run_translate_survey.sh "${path_to_schemas}"/en/"${schema}".json "${parent_dir_path}"/translations/"${schema}"_translate_"${country_code}".xlsx "${path_to_schemas}"/"${country_code}"
      fi
    done < <(find "${parent_dir_path}"/translations -name "*.xlsx" -exec basename {} \;)
}

if [ "$#" -ne 1 ]; then
  echo ""
  echo "Usage: $0 <path_to_schemas>"
  echo ""
  exit 1
fi

path_to_schemas=$1

current_dir_path=$(parent_directory "${BASH_SOURCE[0]}")
parent_dir_path=$(parent_directory "${current_dir_path}")

translate_all_schemas
