#!/bin/bash

# arguments
suffix=""
if [ "$1" != "" ]; then
    suffix="_$1"
fi
if [ "$2" == "dev" ]; then
    suffix+="_$2"
fi

# variables
venv=".venv_connect4$suffix"

# deactivate virtual environment if it's active
if [[ "$venv" == $(basename "$VIRTUAL_ENV") ]]; then
    deactivate
fi

# delete the virtual environment
rm -rf "$venv"

# message indicating the environment is deleted
echo
echo "'$venv' is unset."
