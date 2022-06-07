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
pip install -r requirements.txt && \
echo "Done Installing python requirements"

echo "Starting fEVR"

uwsgi --http 127.0.0.1:${FEVR_PORT:-5090} --wsgi-file fevr.py --callable app --processes ${UWSGI_PROCESSES:-8} --threads ${UWSGI_THREADS:-4} &

TS=0
while [ $TS == 0 ]; do
[ -f "run_mqtt_client.sh" ] && ./run_mqtt_client.sh && sleep 30
done
