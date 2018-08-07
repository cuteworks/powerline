#!/bin/bash

# Credit: https://gist.github.com/trstringer/d8925abf703e875b8df371df41257477#file-run-sh

# Source the virtual environment for systemd or other callers.
SCRIPT_PATH=$(dirname "$(realpath "$0")")
. "$SCRIPT_PATH/venv/bin/activate"
python3 "$SCRIPT_PATH/powerline.py"
