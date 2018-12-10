#!/bin/bash

# Virtual env folder
VENV=venv

if [ ! -d "$VENV" ]; then
  python3 -m venv $VENV
fi

source ./venv/bin/activate
pip install -r requirements.txt
