#!/bin/sh
cd /home/pi/e-ink_hub

python3 /home/pi/e-ink_hub/v1/task_client.py

python3 /home/pi/e-ink_hub/v1/weather.py
python3 /home/pi/e-ink_hub/v1/display.py
