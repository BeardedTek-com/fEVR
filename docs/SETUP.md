# Setup

### Visit http(s)://<fevr_url>/setup

### Create admin account

### Login to new admin account

#### Add all of your cameras.
  - It asks for both HLS and RTSP feeds.  Technically you don't need to enter anything but the camera name, but in a future release live view and frigate config will be enabled and will require these values
  - Click Next

### Configure Frigate
  - make one entry called 'frigate' (without the quotes) with your internally accessible frigate URL
  - make another entry called 'external' (without the quotes) with your externally accessible frigate URL
    - This is 100% Optional.  It does, however, enable live view outside your network.
    - If you don't have an externally accessible frigate URL, you can skip this step.
  - Click Next

### Other 
 - Other is not populated yet, There are future plans for this page, just click Next again and you'll be brought to the main interface.

### Generate API Key for mqtt_client
  - mqtt_client authenticates with fEVR using a 128 character API Key.
  - You can generate an API Key from `/profile` or click on the beard icon to drop down the menu, and click Profile.
  - Here you can view any API keys you have generated in the past and generate a new one.
  - There are 3 fields to fill out:
    - Name: A unique name to identify this key (no duplicates allowed)
    - IPv4 Address: Not used as of now but required to be a valid IP or network (without cidr notation)
      - Enter 0.0.0.0 to future proof.
    - Login Count: this can be used to limit the amount of times this API Key can be used.  While not used at the moment, it will function as the base of a limited login solution (say one time passwords for law enforcement and the like)
      - Enter 0 for unlimited usage

### Configure mqtt_client
  - Once you have your API Key you can generate your config file for the mqtt_client.
    - [See mqtt_client docs here](docs/INSTALL.md) for an example
  - This should be automated further in a later release