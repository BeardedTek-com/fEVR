# fEVR API

## **NOTE**:
Throughout the documentation, any url for fEVR will be listed as ```http://fevr:5090/```.  It is assumed that you will replace this url for your setup.

## Authentication
In order use the API, you must be logged into fEVR.  This can be accomplished by regular login if accessed via a browser, or using an Auth Key.
### Admin Login
- Login as you normally would in any supported web browser at ```http://fevr:5090/login```
### Auth Key
Used to login via the command line or other non-interactive means.  You need to use a cookie jar to save an reuse the session cookie provided by fEVR
Auth Keys can be created at ```http://fevr:5090/profile```
```
curl -X Post http://fevr:5090/apiAuth \
    -c /tmp/fevr_cookiejar
    -H 'Content-Type: application/json' \
    -d '{"key":"FEVR_AUTH_KEY"}'
```
Each subsequent call to the api should reference the cookie jar created.  See API calls below for use.

### **/auth/add/key/`<name>`/`<ip>`/`<limit>`**
Adds an API Key to fEVR with the following parameters:
- name: Name to reference the API Key
- ip: IP Addresses allowed to access key (CIDR Format: 0.0.0.0/0 for all)
- limit: How many times the key can be used (0 for unlimited)
  - if limit is set greater than 1, each time the key is used, this value will be decreased by 1.  If it reaches 0, it will be decreased to -1 and disabled

### **/auth/add/key [POST]**
Adds an API Key using form data with the same parameters as above.


## Setup

### **/api/frigate/add/`<name>`/`<http>`/`<ip>`/`<port>`**
Adds an instance of frigate
  - name: Name as defined to MQTT broker
    - external: if set to external, this is the externally viewable address for frigate (not recommended as it exposes frigate with no authentication)
  - http: set to `http` or `https`
  - ip: IP Address or URL of the frigate server
  - port: Port number frigate is running on (usually 5000)
```
curl http://fevr:5090/api/frigate/add/frigate/http/frigate/5000 \
    -c /tmp/fevr_cookiejar
```
Returns:
```
{
  "name": "frigate", 
  "url": "http://frigate:5000/"
}
```

### **/api/cameras/add/`<camera>`/`<server>`/`<show>`**
Adds a camera to fEVR
  - camera: camera name
  - server: ip or url of rtsp-simple-server
    - rtsp-simple server is not required for fEVR functionality
    - Future releases will further integrate with rtsp-simple-server or some custom solution.  If you wish to future proof, you can use the server name ```rtsp```.
  - show: show in all/latest views (useful for indoor or sensitive areas)
    - set to "true" or "True" otherwise it will be False.
```
curl http://fevr:5090/api/cameras/add/front/rtsp/true \
    -c /tmp/fevr_cookiejar
```

## Adding or Modifying Events

### **/api/events/add/`<eventid>`/`<camera>`/`<object>`/`<score>`**
Adds an event from Frigate

**NOTE**: This is what mqtt_client uses to insert data into fEVR.  While you can insert data by looking at frigate, it is not necessary unless mqtt_client fails or you want to archive a non-qualified event.
  - eventid: Event ID from frigate
  - camera: Name of camera as defined in fEVR
  - object: Object name (person, vehicle, etc)
  - score: Score (as an integer) as provided by frigate
```
curl http://fevr:5090/api/events/add/1657137967.016307-5qek8n/front/person/84 \
    -c /tmp/fevr_cookiejar
```
Return if OK:
```
{
  "camera": "front", 
  "error": 0, 
  "eventid": "1657137967.016307-5qek8n", 
  "msg": "", 
  "object": "person", 
  "score": "84", 
  "time": "Wed, 06 Jul 2022 20:06:07 GMT"
}
```
Return if Camera Not Defined:
```
{
  "error": 1,
  "msg": "Camera Not Defined
}
```
Return if Event Exists:
```
{
  "camera": "front", 
  "error": 2, 
  "eventid": "1657137967.016307-5qek8n", 
  "msg": "Event Already Exists", 
  "object": "person", 
  "score": "84", 
  "time": "Wed, 06 Jul 2022 20:06:07 GMT"
}
```
Return if Event Does Not Exist:
```
{
  "error": 3, 
  "msg": "Unable to Fetch Event"
}
```
### **/api/events/ack/`<eventid>`**
Acknowledge an Event
  - eventid: Event ID from frigate
```
curl http://fevr:5090/api/events/ack/1657137967.016307-5qek8n \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "msg": "Success"
}
```
Return if Failed:
```
{
  "error": 1,
  "msg": "Failed"
}
```

### **/api/events/unack/`<eventid>`**
Unacknowledge an Event
  - eventid: Event ID from frigate
```
curl http://fevr:5090/api/events/unack/1657137967.016307-5qek8n \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "msg": "Success"
}
```
Return if Failed:
```
{
  "error": 1,
  "msg": "Failed"
}
```

## Retrieve Information

### **/api/frigate**
Returns information about configured frigate instances
```
curl http://fevr:5090/api/frigate \
    -c /tmp/fevr_cookiejar
```
Returns:
```
{
  "1": {
    "name": "frigate", 
    "url": "http://frigate:5000"
  }
}
```

### **/api/cameras/`<camera>`**
Returns information about cameras in JSON
  - use all to get info on all cameras
  - use camera name to get info on specific camera
```
curl http://fevr:5090/api/cameras/front \
    -c /tmp/fevr_cookiejar
```
Returns:
```
{
  "front": {
    "camera": "front", 
    "hls": "http://rtsp:5084/front", 
    "id": 1, 
    "rtsp": "rtsp://rtsp:5082/front", 
    "show": true
  }
}
```

### **/api/events/latest**
Displays the last 12 events
```
curl http://fevr:5090/api/events/latest \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "8070": {
    "ack": "", 
    "camera": "front", 
    "eventid": "1657328017.442961-lpdap6", 
    "object": "person", 
    "score": 75, 
    "show": false, 
    "time": "Sat, 09 Jul 2022 00:53:37 GMT"
  },

    ...

  "8083": {
    "ack": "", 
    "camera": "front", 
    "eventid": "1657329656.072334-0sggw2", 
    "object": "person", 
    "score": 73, 
    "show": false, 
    "time": "Sat, 09 Jul 2022 01:20:56 GMT"
  }
}
```

### **/api/events/all**
Displays all events
```
curl http://fevr:5090/api/events/latest \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "1": {
    "ack": "", 
    "camera": "front", 
    "eventid": "1655439416.135376-md3t78", 
    "object": "person", 
    "score": 76, 
    "show": false, 
    "time": "Fri, 17 Jun 2022 04:16:56 GMT"
  }, 

    ...

  "8083": {
    "ack": "", 
    "camera": "back", 
    "eventid": "1657329686.811457-xkj95z", 
    "object": "person", 
    "score": 70, 
    "show": false, 
    "time": "Sat, 09 Jul 2022 01:21:26 GMT"
  }
}
```

### **/api/events/camera/`<camera>`**
Displays all events from a camera
```
curl http://fevr:5090/api/events/camera/front \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "1": {
    "ack": "", 
    "camera": "front", 
    "eventid": "1655439416.135376-md3t78", 
    "object": "person", 
    "score": 76, 
    "show": false, 
    "time": "Fri, 17 Jun 2022 04:16:56 GMT"
  }, 

    ...

  "8084": {
    "ack": "", 
    "camera": "front", 
    "eventid": "1657329686.811457-xkj95z", 
    "object": "person", 
    "score": 70, 
    "show": false, 
    "time": "Sat, 09 Jul 2022 01:21:26 GMT"
  }
}
```
### **/api/event/`<eventid>`**
Displays information about an event
  - eventid: Event ID from frigate
```
curl http://fevr:5090/api/event/1657329686.811457-xkj95z \
    -c /tmp/fevr_cookiejar
```
Return:
```
{
  "8084": {
    "ack": "", 
    "camera": "back", 
    "eventid": "1657329686.811457-xkj95z", 
    "object": "person", 
    "score": 70, 
    "show": false, 
    "time": "Sat, 09 Jul 2022 01:21:26 GMT"
  }
}
```

# **The following API Calls are intened to be used from the UI Only.**

## Deleting Events

### **/api/events/del/`<eventid>`**
Deletes an Event
**NOTE**: This api call is intended to be used from the UI only.  There are no checks to acknowledge deleting this event.
  - eventid: Event ID from frigate
```
curl http://fevr:5090/api/events/del/1657137967.016307-5qek8n \
    -c /tmp/fevr_cookiejar
```
Return:
```
Returns user to last page
```
