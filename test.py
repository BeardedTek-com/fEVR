#!/usr/bin/python3
from os import getenv
mqttOpts = {}
opts = {"broker":"MQTT_BROKER_URL",
        "port":"MQTT_BROKER_PORT",
        "username":"MQTT_USER",
        "password":"MQTT_PASS",
        "topics": "MQTT_TOPICS"}
for opt in opts:
    mqttOpts[opt] = getenv(opts[opt])
    if mqttOpts[opt] == None:
        mqttOpts[opt] = ''
    else:
        if opt == 'topics':
            topics = []
            topicList = mqttOpts['topics'].split(',',2)
            x=0
            for topic in topicList:
                if x == 2:
                    print(f"Topic Limit Exceeded. Topics included: {topics}")
                    break
                else:
                    topics.append(topic)
                    x+=1
            mqttOpts[opt] = topics
            


broker = opts['broker']
port = opts['port']
username = opts['username']
password = opts['password']
topics = opts['topics']
print(f"fevrMQTT({mqttOpts['broker']},{mqttOpts['port']},{mqttOpts['topics']},username={mqttOpts['username']},password={mqttOpts['password']})")