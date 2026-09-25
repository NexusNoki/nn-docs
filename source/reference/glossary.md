# Glossary

```{glossary}
Border router
  A device that links the Thread mesh to your home network. In nn this is the {term}`gateway`.

Catalog
  The list of firmware images the hub can flash and update devices with. Filled from
  {term}`sources <Source>`.

FreeRTOS camera
  A microcontroller camera, such as the ESP32-P4. It streams video; the media server runs the
  detection.

Gateway
  The nn border router: a Linux program plus an ESP32-C6 {term}`NCP` radio. It runs on the hub
  or on a {term}`Linux camera`.

HLS
  HTTP Live Streaming. The video format the web app plays in the browser.

Hub
  The always-on service at the centre of nn: web app, device database, catalog, provisioning,
  automations and updates.

Linux camera
  A camera running a small Linux system, such as the BeagleY-AI. It runs detection itself, updates
  its system in two slots, and can host a {term}`gateway`.

Media server
  The service that receives camera video, makes the live view and HLS, and runs detection.
  Its program is called nnvideo.

NCP
  Network co-processor. An ESP32-C6 running only the Thread radio, driven over USB by the
  gateway.

NPU
  Neural processing unit. The chip block that runs the object detector fast and at low power.

OTA
  Over-the-air update: new firmware delivered over the network instead of a cable.

Promote
  Make a catalog version the target that devices of that type should run.

Provisioning
  Giving a new device its network settings and keys, over Bluetooth, from the hub.

Setup mode
  The state of a device that is not provisioned: it advertises over Bluetooth so the hub can
  find it.

Source
  A place the hub checks for firmware releases, such as a GitHub releases page.

Thread
  A low-power IPv6 mesh radio network. nn sensors use it.
```
