#!/bin/bash

DIR="/home/pi/calorimetro"

cd "$DIR"

source "$DIR/venv/bin/activate"

export FLASK_APP=app.py
python -m flask run --host=0.0.0.0 &
#python temperatura_y_leds.py &
