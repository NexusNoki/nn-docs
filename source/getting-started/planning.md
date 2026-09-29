# Plan your installation

Before you install anything, decide which machine does which job, and check you have the parts.

## The four roles

nn is made of four roles. They can all run on **one machine**, which is how this tutorial sets
them up, or be spread across several.

| Role | What it does | Runs on |
|---|---|---|
| **Hub** | The web app, the device database, the firmware catalog, provisioning over Bluetooth, automations, over-the-air updates | one always-on Linux machine |
| **Media server** | Receives camera video, makes live view and HLS, runs motion and object detection, records events | the hub machine, or a machine with a hardware video codec and an NPU |
| **Thread gateway** | The border router between the Thread mesh the sensors use and your home network | a USB radio on the hub, or a Linux camera (BeagleY-AI) |
| **Devices** | Cameras and sensors | their own boards |

:::{tip}
Start with everything on one machine. Moving the media server or the gateway to another machine
later does not change your cameras' or sensors' settings.
:::

## Recommended hardware

### Hub (and media server)

| Machine | Status | Notes |
|---|---|---|
| **Orange Pi 6 Plus** (CIX P1) | **supported — used in this tutorial** | hardware H.264 codec and a Zhouyi NPU, so it can also be the media server |
| Mac mini | planned | see {doc}`hub/other-platforms` |
| x86 PC | planned | see {doc}`hub/other-platforms` |
| Raspberry Pi | planned | see {doc}`hub/other-platforms` |

The hub needs a **Bluetooth Low Energy** radio. It uses it to provision every new camera and
sensor. The Orange Pi 6 Plus has one on board, but it needs its antenna fitted (see
{doc}`hub/orange-pi-6-plus`); a USB Bluetooth adapter works too.

### Cameras

nn camera firmware is built for a specific board **and a specific image sensor**. An image only
works with the sensor it was built for, so choose the board and sensor together.

| Kind | Board | Image sensor | Page |
|---|---|---|---|
| FreeRTOS camera | Waveshare ESP32-P4-WIFI6 | OV5647 | {doc}`cameras/esp32-p4` |
| FreeRTOS camera | Waveshare ESP32-P4-Module-DEV-KIT (ESP32-C6 on board) | OV5647 | {doc}`cameras/esp32-p4` |
| Linux camera | BeagleY-AI | Raspberry Pi Camera Module 3 **Wide NoIR** (IMX708) only | {doc}`cameras/beagley-ai` |

### Thread radio and sensors

| Part | Used for |
|---|---|
| ESP32-C6 board with the **NCP** firmware | the gateway's Thread radio, on USB |
| ESP32-C6 boards with the **sensor** firmware | the example sensors (button and switch) |

See {doc}`gateway` and {doc}`sensors/index` for the exact boards.

## Your network

- Give the hub a **fixed address** (a DHCP reservation in your router). This tutorial uses
  `@@hub_ip@@`.
- Cameras need Wi-Fi (2.4 GHz). Have the network name and password ready: you type them into the
  hub once per device, and the hub hands them over Bluetooth.
- All nn traffic stays on your network. See {doc}`/reference/ports` for every port.

## What you need for this tutorial

- [ ] Orange Pi 6 Plus with power supply, antenna and a microSD card or NVMe for the OS
- [ ] a computer with a browser on the same network
- [ ] a USB cable for each device you will flash (USB-C for the ESP32 boards)
- [ ] a USB microSD card reader, if you set up a BeagleY-AI camera
- [ ] at least one camera from the table above
- [ ] one ESP32-C6 for the gateway radio and two or three for sensors
