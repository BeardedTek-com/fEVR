# fEVR - frigate Event Video Recorder

## Development has ceased on this project.  Frigate has matured to a pint where I feel this is no longer necessary.

[![license](https://img.shields.io/github/license/beardedtek-com/fevr)](https://github.com/BeardedTek-com/fevr/blob/0.1.0/LICENSE)
[![telegram](https://img.shields.io/badge/Support-Telegram-blue)](https://t.me/BeardedTekfEVR)
[![Discussions](https://img.shields.io/github/discussions/beardedtek-com/fevr)](https://github.com/BeardedTek-com/fEVR/discussions)
[![commits since last release](https://img.shields.io/github/commits-since/beardedtek-com/fevr/latest?include_prereleases)](https://github.com/BeardedTek-com/fEVR/releases)
[![Build Status](https://drone.beardedtek.com/api/badges/BeardedTek-com/fEVR/status.svg)](https://drone.beardedtek.com/BeardedTek-com/fEVR)
[![Image Size](https://img.shields.io/docker/image-size/beardedtek/fevr)](https://hub.docker.com/r/beardedtek/fevr)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fbeardedtek-com%2Ffevr)](https://twitter.com/intent/tweet?url=https%3A%2F%2Ffevr.video&text=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder)
[![twitter-follow](https://img.shields.io/twitter/follow/beardedtek?style=social)](https://twitter.com/intent/user?screen_name=beardedtek)

[![Pinterest](https://img.shields.io/badge/Share-Pin%20It!-e60023)](http://pinterest.com/pin/create/button/?url=http%3A%2F%2Ffevr.video&media=&description=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder)
[![Reddit](https://img.shields.io/badge/Share-Reddit-orange)](https://reddit.com/submit?url=https://fevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder)
[![LinkedIn](https://img.shields.io/badge/Share-LinkedIn-blue)](http://www.linkedin.com/shareArticle?mini=true&url=http%3A%2F%2Ffevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder)
[![Donate - Paypal](https://img.shields.io/badge/Donate-Paypal-0070e0)](https://www.paypal.com/donate/?hosted_button_id=ZAHLQF24WAKES)
[![Donate - GitHub](https://img.shields.io/badge/Donate-GitHub%20Sponsors-blue)](https://github.com/sponsors/BeardedTek-com)
[![Donate - Tallyco.in](https://img.shields.io/badge/Donate-Tallyco.in-fdc948)](https://tallyco.in/s/waqwip/)

fEVR works along side of [frigate](https://frigate.video) to collect video and snapshots of objects detected using your existing camera systems.
<p align="center">
<img alt="fEVR v0.6 Screenshots" src="https://user-images.githubusercontent.com/93575915/165704583-fec8e202-88b8-4ca2-9ff2-345c04da3722.png">
</p>
<p align="center">
fEVR v0.6 Screenshots
</p>

# Own Your Home's Security

fEVR allows you to own your home's camera system.  Instead of paying multiple cloud providers varying rates to perform object detection and recording, bring them all into fEVR in your very own open source self-hosted solution!  Google, Wyze, Ring, and varying Tuya based cameras all use your data AND want to charge you to store it in the cloud.
<p align="center">
<img alt="Feature comparison to leading cloud event detection providers" src="docs/images/features.webp">
</p>
<p align="center">
Feature comparison to leading cloud event detection providers
</p>

---

# Requirements:
- Frigate fully setup and working
- MQTT Broker (if you have frigate running, you have this) listening to 0.0.0.0
  - This caused me many headaches, hopefully it saves you some hair pulling.
    It allows mqtt clients on different subnets to access the broker.
    If setup within your local lan this does not alone open up external access, only to other subnets which already have access.
  - Example mosquitto.conf listener section if using port 1883
    ```
    listener 1883 0.0.0.0
    ```

## Optional but nice:
- Tailscale Account (for secure remote access)

---

# Documentation
A special thanks to @renarena for help with proofreading docs

## [Installation - docs/INSTALL.md](docs/INSTALL.md)
## [Setup - SETUP.md](docs/SETUP.md)
## [More Info on mqtt_client - MQTT_CLIENT.md](docs/MQTT_CLIENT.md)

## [Main API Calls](docs/API.md)

## [Tutorial Videos](https://beardedtek.net/c/tutorials/videos)

## [Notifications](docs/NOTIFICATIONS.md)

---

# Support
Please note, I will generally answer questions within 24 hours, and most times even faster unless I'm on vacation or going on adventures with the family.

## [Submit an Issue](https://github.com/BeardedTek-com/fEVR/issues)
This is the preferred method if you find an error in the code or something that crashes fEVR.
  
## [Start a discussion](https://github.com/BeardedTek-com/fEVR/discussions)
For discussing configuration issues or things that bug you (UI tweaks or process improvements)
  
## [Telegram Support Channel](https://t.me/BeardedTekfEVR)
## [Matrix Support Space](https://matrix.to/#/#fevrsupport:matrix.org)
For troubleshooting, a quick question, or you just want to say hi!


---
# Development
## Main Branch
The main branch is the current release branch.  When I do a release on 0.6 it will be merged to here.

## 0.6 Branch
Each major version will have its own branch.  This is the current gold standard for the newest release in 0.6

## 0.6-dev Branch
This is the development branch for v0.6  Any changes will be added here before being merged with the 0.6 Branch

## 0.7-dev Branch
This is the development branch for the next version.  If it introduces breaking changes, it belongs here.

# Releases
## Docker
**docker compose** is the recommended method to deploy fEVR

#### GitHub Container Repository ghcr.io (preferred location)
ghcr.io/beardedtek-com/fevr
#### Docker Hub
beardedtek/fevr

The following tags are available:
- **RECOMMENDED**
  - latest
    - This contains the latest release in the current stable branch

  - 0.6
    - This contains the latest release in the 0.6 branch

- **NOT RECOMMENDED**
  - 0.6-dev 
    - Latest development image in the 0.6 branch.  This could potentially change a couple times a day when under heavy development.
  - 0.7-dev **NOT RECOMMENDED**
    - Bleeding Edge and almost guaranteed to contain **breaking changes**

## PyPi
### **NOT RECOMMENDED**
I'm starting to release some code on pypi as I break a few things apart for the 0.7 branch.  Use at your own risk.  It may or may not work as intended for now and breaking changes are certainly coming before this is an official release channel.
