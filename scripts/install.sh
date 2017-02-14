#!/usr/bin/env bash

function parent_directory {
    current_dir=$(dirname "$1")
    parent_dir="$( cd "${current_dir}" && pwd )"
    echo $parent_dir
}

current_dir_path=$(parent_directory "${BASH_SOURCE[0]}")
parent_dir_path=$(parent_directory "${current_dir_path}")

source "$(which virtualenvwrapper.sh)"
virtual_envs=$(lsvirtualenv -b)

if [[ "${virtual_envs}" != *"eq-translations"* ]]; then
    echo "Creating new eq-translations virtual environment"
    mkvirtualenv --python="$(which python3)" eq-translations
    workon eq-translations
    pip install -r "${parent_dir_path}"/requirements.txt
else
    echo "Using existing eq-translations virtual environment"
    workon eq-translations
    pip install -r "${parent_dir_path}"/requirements.txt
fi