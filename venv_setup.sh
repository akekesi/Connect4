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
python_required="Python 3.12.0"
python_current=$(python --version 2>&1)
requirements="requirements.txt"
requirements_dev="requirements_dev.txt"

# python version check
if [[ "$python_current" != *"$python_required"* ]]; then
    echo "Virtual environment '$venv' is not created."
    echo "Python version current:  $python_current"
    echo "Python version required: $python_required"
    return 0
fi

# create virtual environment
if [ ! -d "$venv" ]; then
    python -m venv "$venv"
else
    echo "Virtual environment '$venv' already exists."
    return 0
fi

# activate virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    . "$venv/Scripts/activate"
else
    echo "Virtual environment '$venv' is already activated."
    return 0
fi

# upgrade pip and install requirements
python -m pip install --upgrade pip > /dev/null
pip install -r "$requirements" > /dev/null

# install development requirements if "dev" argument is passed
if [ "$2" == "dev" ]; then
    pip install -r "$requirements_dev" > /dev/null
fi

# deactivate virtual environment
if [[ ! -z "$VIRTUAL_ENV" ]]; then
    deactivate
fi

# message indicating the setup is complete
echo
echo "'$venv' is set up."
echo "Command to activate or deactivate '$venv':"
echo "Activation:   . $venv/Scripts/activate"
echo "Deactivation: deactivate"
