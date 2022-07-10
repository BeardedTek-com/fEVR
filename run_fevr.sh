#!/bin/bash
#    This code is a portion of frigate Event Video Recorder (fEVR)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

[ ! -d "/fevr/venv" ] && \
    echo "Initializing Virtual Environment" && \
    python -m venv venv && \
    echo "Starting Virtual Environment" && \
    source /fevr/venv/bin/activate \
|| \
    echo "Python Virtual Environment already installed."
    echo "Activating Python Virtual Environment"
    source /fevr/venv/bin/activate

echo "Starting fEVR"
uwsgi --http 127.0.0.1:${FEVR_PORT:-5090} --wsgi-file fevr.py --callable app --processes ${UWSGI_PROCESSES:-8} --threads ${UWSGI_THREADS:-4} &

TS=0
while [ $TS == 0 ]; do
[ -f "run_mqtt_client.sh" ] && ./run_mqtt_client.sh && sleep 30
done
