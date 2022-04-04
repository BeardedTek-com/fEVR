# Open Source Software

Following the Unix/Linux Pipe Philosophy, fEVR builds upon state of the art open source technology

- [Tensorflow](tensorflow.org)
  - Most commercial object detection systems use Tensorflow as its base.
  - Requires extensive knowledge of programming to adapt it for your own use
- [Frigate](https://frigate.video)
  - Builds upon Tensorflow and makes tuning object detection easy for the masses
  - Requires extensive research to get a config.yml file generated
- fEVR
  - Provides an interface to easily configure Frigate
  - Easily view events
  - Easily share events with family, friends
  - Provide law enforcement with a downloadable link with an auto expiring password (coming soon)
  - Secure remote viewing using [Tailscale](https://tailscale.com)
  - Secure login system (coming soon)

# What is an EVR?

EVR is a new term for a smarter camera system.  Security Cameras have evolved over the years.

- Standalone:
  - Standalone systems were viewed on a monitor with no way to record footage
- VCR Systems:
  - With the advent of the VCR, people began recording camera feeds continuously.  In order to view footage, you would have to stop recording and rewind to view it.
- DVR Systems:
  - Still using outdated analog cameras, a DVR or Digital Video Recorder records analog footage to a hard drive.  Systems began only recording when motion is detected saving some space, but still recording hours of footage because of static induced by interference, grainy subpar quality video, or a fly zipping by the camera.
- NVR Systems:
  - Using updated technology, digital cameras could now reduce interference, but are still mainly based on motion.  A few NVR's try to use object detecion, but most end-users and even professional installers don't understand the settings to make full use of the technology.
- EVR:
  - Event Video Recorders focus on events rather than motion or continuous recording.  While both are still available, EVR's generally have lower storage requirements.

- Comparison: (All systems configured with 1TB of storage, 1080p cameras, and typical configuration for model type)
  - DVR: 1 week continuous and 2 weeks of motion recordings
    - Subpar quality due to interference induced by power, communication circuits, even WiFi and Cell Phones
    - Low quality continuous recording and higher quality motion detection
      - You know its a person and might have an idea who they are, can not read license plates
  - NVR: 2 weeks of continuous video and 1 month of motion recording
    - Better quality but usually heavy compression to save space which degrades quality and clearness of details
      - Can almost make out license plates, but you can identify a person's identifying marks
    - Details are smudged and still grainy
    - Higher quality continuous recording and more advanced motion detection
  - EVR: 1-2 days continuous and 1 year of object recording
    - Full 1080p resolution with very little compression which makes for a better image and longer retention
      - Can see details such as license plates, hair color, clothing, tattoos, etc

# Cost

Security cameras that support object detection natively without the cloud are expensive.
- Hikvision:
  - 1080p AcuSense cameras start at $150 each
  - AcuSense DVR (required if you want to save data easily) start at $450 used
  - Cost for 4 camera system: $1050
- Lorex:
  - 1080p Smart Deterrence cameras start at $130 each
  - N Series NVR: $300
  - Cost for 4 camera system: $950

- fEVR + Wyze:
  - Wyze Cam v3: $35
  - fEVR box: $299.99 (projected price)
  - Cost for 4 camera system: $439.99