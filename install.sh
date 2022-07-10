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

release=$(lsb_release -d)
if [ $(echo $release | awk -F' ' '{print $2}') == "Ubuntu" ]; then
    vers=$(echo $release | awk -F' ' '{print $3}')
    if [ $vers == "22.04" ] || [ $vers == "20.10" ] || [ $vers == "21.04" ] || \
    [ $vers == "20.04" ]; then
        echo "Installing for Ubuntu > 20.04"
        DEBIAN_FRONTEND=noninteractive sudo apt-get update && \
        sudo apt-get -y --no-install-recommends install python3.10 \
        python-is-python3 python3-pip

        python3 -m venv venv
        source venv/bin/activate
        python3 -m pip install -r requirements.txt
    fi
elif [ $(echo $release | awk -F' ' '{print $2}') == "openSUSE" ]; then
    echo "Installing for openSUSE"
    sudo zypper --non-interactive --no-recommends install python310-pip
    if [ ! -d venv ]; then
        python3.10 -m venv venv
    fi
    python3.10 -m pip install -r requirements.txt
else
    echo "Your distro is not supported yet."
    echo "Currently supported distros:"
    echo " - openSUSE: Tested on Tumbleweed"
    echo " - Ubuntu >= 22.04: Tested on 22.04 Server"
    echo ""
    echo "Requirements:"
    echo " - python >= 3.8 (3.10 recommended)"
    echo " - pip3"
    echo " - create virtual environment"
    echo " - pip install -r requirements.txt"
fi
pythonversion=$(python --version)
pythonver=$(echo $pythonversion | awk -F' ' '{print $2}')
pymaj=$(echo $pythonver | awk -F'.' '{print $1}')
pymin=$(echo $pythonver | awk -F'.' '{print $2}')

# Start checks to see if requirements are satisfied
clear
echo "fEVR Installation Script Results:"
echo ""
if [ $pymaj == "3" ]; then
    if [[ $pymin -gt 8 ]]; then
        echo -e "[\e[32mPASS\e[39m] $pythonver"
        pipver=$(pip3 --version)
        if [ $(echo $pipver | awk -F ' ' '{print $1}') ]; then
            echo -e "[\e[32mPASS\e[39m] $pipver"
        else
            echo -e "[\e[31mFAIL\e[39m] $pipver"
            installchk="FAIL"
        fi
    else
        echo -e "[\e[31mFAIL\e[39m] $pythonver"
        installchk="FAIL"
    fi
fi

if [ -d venv ]; then
    echo -e "[\e[32mPASS\e[39m] venv exists"
    uwsgiver=$(source venv/bin/activate && uwsgi --version)
    if [ $(echo $uwsgiver | awk -F'.' '{print $1}') == "2" ]; then
        echo -e "[\e[32mPASS\e[39m] $uwsgiver"
    fi
else
    echo -e "[\e[31mFAIL\e[39m] venv does not exist"
    echo -e "[\e[31mFAIL\e[39m] No Virtual Environment"
    installchk="FAIL"
fi
echo ""
if [ "$installchk" == "FAIL" ]; then
    echo -e "[\e[31mFAIL\e[39m] Checks failed"
    echo ""
    echo "Please correct failures above manually."
else
    echo -e "[\e[32mPASS\e[39m] Installation Successful"
fi