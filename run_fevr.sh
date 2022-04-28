#!/bin/bash
[ ! -d "/fevr/venv" ] && \
    echo "Initializing Virtual Environment" && \
    python -m venv venv && \
    echo "Starting Virtual Environment" && \
    source /fevr/venv/bin/activate \
|| \
    echo "Python Virtual Environment already installed."
    echo "Activating Python Virtual Environment"
    source /fevr/venv/bin/activate

# Install Dependencies
echo "pip install wheel" && \
pip install wheel && \
echo "pip install requirements" && \
pip install -r /fevr/app/requirements.txt && \
echo "Done Installing python requirements"

echo "Starting fEVR"
# Uncomment to put fEVR into development Mode
#export FLASK_ENV='development'

/fevr/venv/bin/flask run -h "0.0.0.0" -p 5090

TS=0
while [ $TS == 0 ]; do
    sleep 10000
done
