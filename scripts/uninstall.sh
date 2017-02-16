#!/usr/bin/env bash

# Try to deactivate python env but don't complain if not in virtual env
deactivate > /dev/null 2>&1 || true
source "$(which virtualenvwrapper.sh)"
rmvirtualenv eq-translations