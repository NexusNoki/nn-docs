# Philosophy

Four ideas shape every decision in nn.

## Local first, no cloud

Your video, your sensor readings and your automations stay in your home. The hub, the media
server and the devices talk to each other on your own network; the internet is optional. When
your connection drops, everything keeps working: cameras record, sensors report, lights switch.
If you want to look in from outside, you add that yourself (see {ref}`remote-access`), behind your
own login.

## You own the firmware

Every device runs firmware you can rebuild from the public source, and update over the air from
your own hub. There is no vendor account to register, no locked bootloader, and no update server
that can disappear. The hub signs and serves updates; a device only runs an image it can verify,
and falls back to the previous one if the new one fails.

## The devices act on their own

Sensors do not wait for a server to decide what to do. Automations are compiled on the hub and
pushed to the devices, which run them over the Thread mesh themselves: a button still switches a
lamp when the hub is off or restarting. The hub watches, fills in what the radio missed, and
keeps the history.

## Cheap, off-the-shelf boards

nn runs on boards anyone can buy: ESP32 modules, a BeagleY-AI, an Orange Pi. No proprietary
hub, no special radios. That keeps the cost low, lets you replace a broken part yourself, and
means the knowledge you gain carries over to other projects.
