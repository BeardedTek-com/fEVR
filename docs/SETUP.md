# Setup

### Visit http(s)://<fevr_url>/setup
 
 
### Create admin account
 
 
### Login to new admin account
 
 
#### Add all of your cameras.
Enter your camera's name as it is defined in Frigate.
HLS and RTSP fields are not yet used, but will be in 0.7

Click Next

***NOTE:** I recommend using an rtsp relay that way you only have 1 connection to your cameras, reducing bandwidth use and minimizing connections to your rtsp devices.*

##### Popular Open Source RTSP Relays:
[rtsp-simple-server](https://github.com/aler9/rtsp-simple-server)
[docker-wyze-bridge](https://github.com/mrlt8/docker-wyze-bridge) < uses rtsp-simple-server at its core

### Configure Frigate MQTT Settings
Frigate allows you to change the mqtt topic for hosting multiple servers on the same mqtt broker.  Unless you have changed this default behavior or have multiple frigate servers on one broker, name this entry frigate and fill in the server's details.

Click Next

### Other 
Other is not populated yet, There are future plans for this page, just click Next again and you'll be brought to the main interface.

### Generate API Key for mqtt_client
mqtt_client authenticates with fEVR using a 128 character API Key.

You can generate an API Key from `/profile` or click on the beard icon to drop down the menu, and click Profile.

Here you can view any API keys you have generated in the past and generate a new one.

There are 3 fields to fill out:
**Name:** A unique name to identify this key (no duplicates allowed)
**IPv4 Address:** Not used as of now but required to be a valid IP or network (without cidr notation)
- Enter 0.0.0.0 to future proof.

**Login Count:** this can be used to limit the amount of times this API Key can be used.  While not used at the moment, it will function as the base of a limited login solution (say one time passwords for law enforcement and the like)
- Enter 0 for unlimited usage

### Configure mqtt_client
Once you have your API Key you can generate your config file for the mqtt_client.
  - See [Installation](/installation) for an example

This will be automated further in a future release.