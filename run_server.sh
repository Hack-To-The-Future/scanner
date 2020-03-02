#!/bin/bash -e

trap 'kill $(jobs -p)' EXIT

py=/home/pi/.cache/pypoetry/virtualenvs/scanner-Xb41yQIt-py3.7/bin/python3
$py scanner/manage.py runserver 0.0.0.0:8000 &
sleep 5
cd inference
$py inference.py &
wait