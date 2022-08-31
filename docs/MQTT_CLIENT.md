# mqtt_client

mqtt_client is an integral part of fEVR.  It functions as the link between fEVR and frigate.

# Features
- Can run on any host that can reach fEVR
- Configurable by yaml, json, or command line arguments

# What is it doing?
- Loads config from either yaml, Json, command line arguments, or leaves the default
    - Priority:
        1. Command Line Argument
        2. Config File
        3. Defaults
    - Defaults:
        - 'fevr': "localhost:5090"
        - 'mqtt_broker': "mqtt"
        - 'mqtt_port': 1883
        - 'mqtt_user': ''
        - 'mqtt_password': ''
        - 'mqtt_apikey': ''
        - 'verbose': False
        - 'fevr_transport': 'http://'
        - 'mqtt_topics': "frigate/+"
- Connects to MQTT Broker
- Subscribes to topics
- Listens for frigate/events
    - When it sees an event type of "end" it connects to fEVR's API
        - sends an http request to **http(s)://`<fevr_host>`:`<fevr_port>`/api/events/add/`<eventid>`/`<camera>`/`<object>`/`<score>`**
        - waits for a response from fEVR's API
        - goes back to listening

# Why is it a separate program?
- If mqtt_client fails, it can restart itself independently of fEVR so it does not take down the entire stack.

# Configuration

## Yaml
Here is a sample yaml configuration file:
[yaml 1.2 specification](https://yaml.org/spec/1.2.2/)
[yamllint.com](https://yamllint.com) - Test to see if your yaml is properly formatted.
```
fevr_host: localhost
fevr_port: 5090
fevr_transport: http://
mqtt_broker: mqtt
mqtt_port: 1883
mqtt_user: ~
mqtt_password: ~
mqtt_topics:
    - frigate/available
    - frigate/events
    - frigate/stats
mqtt_apikey: 128-bit-apikey-from-fevr
verbose: true
```
## Json
Here is a sample Json configuration file:
```
# See the docs for setup instructions
{
    "fevr_host": "localhost",
    "fevr_port": 5090,
    "fevr_transport": "http://",
    "mqtt_broker": "mqtt",
    "mqtt_port": 1883,
    "mqtt_user": null,
    "mqtt_password": null,
    "mqtt_topics": ["frigate/available","frigate/events","frigate/stats"],
    "mqtt_apikey": "128-char-apikey-from-fevr",
    "verbose": true
}
```

## Command Line

**(venv) user@localhost:~> *mqtt_client -h***
```
usage: mqtt_client [-h] [-c CONFIG] [-m MQTT] [-k KEY] [-p PORT] [-t TOPICS] [-u USER] [-P PASSWORD] [-f FEVR] [-s] [-v]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        If set, uses command line options instead of the database (default: empty)
  -m MQTT, --mqtt MQTT  MQTT Broker IP/FQDN (default: mqtt)
  -k KEY, --key KEY     fEVR API Key (default: blank string)
  -p PORT, --port PORT  MQTT Port (default: 1883)
  -t TOPICS, --topics TOPICS
                        MQTT Topics (default: 'frigate/+')
  -u USER, --user USER  MQTT Username (default: '')
  -P PASSWORD, --password PASSWORD
                        MQTT Password (default: '')
  -f FEVR, --fevr FEVR  fEVR IP Address/FQDN (default: '127.0.0.1:5090)
  -s, --https           If set uses https:// for fEVR API Calls (default: False)
  -v, --verbose         If set, outputs verbosely to stdout
```