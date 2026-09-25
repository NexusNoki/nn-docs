# Set up cameras

An nn camera streams its video to the media server over your Wi-Fi. It talks to the hub with
its own keys, which it receives when you provision it. Every camera goes through the same three
steps:

1. **Add its image to the catalog**, so the hub knows the firmware.
2. **Flash** the image: over USB for ESP32-P4 boards, onto a microSD card for the BeagleY-AI.
3. **Provision and register** it from the hub's **Add device** wizard, over Bluetooth.

nn has two kinds of camera:

- a **FreeRTOS camera** (for example the ESP32-P4) is a small microcontroller camera. It sends
  video, and the media server runs the detection;
- a **Linux camera** (for example the BeagleY-AI) runs detection itself, updates its whole
  system safely over the air, and can also be a Thread gateway.

## Choose the image for your sensor

:::{important}
Each camera image is built for **one board and one image sensor**. An image does not detect
the sensor: with any other camera module it fails to start the camera. Check both the board
and the sensor before you flash.
:::

**Supported**

| Board | Image sensor | Image |
|---|---|---|
| Waveshare ESP32-P4-WIFI6 (chip rev. v3.1) | OV5647 (Raspberry Pi Camera v1.3 class) | `@@rel_cam_p4_wifi6@@` |
| Waveshare ESP32-P4-Module-DEV-KIT (chip rev. v1.3) | OV5647 | `@@rel_cam_p4_module@@` |
| BeagleY-AI | Raspberry Pi Camera Module 3 **Wide NoIR** (IMX708) | `@@rel_byai_sdcard@@` |

**Experimental** (not covered by this tutorial)

| Board | Image sensor | Image |
|---|---|---|
| Waveshare ESP32-P4-Module-DEV-KIT | IMX708 | `nn-app-camera-esp32p4module-sdio-imx708` |
| ESP32-P4 with a separate ESP32-C6 over SPI | IMX708 | `nn-app-camera-esp32p4c6-spi-imx708` |

```{todo}
Confirm which camera images will be published as releases, and add their names as variables in
`conf.py` like the supported ones. Confirm whether the BeagleY-AI image also works with the
standard (non-Wide, non-NoIR) Camera Module 3.
```

## Add camera images to the catalog

The hub reads firmware from **sources** (see {doc}`/getting-started/sensors/index` for how to add
a GitHub source in **Factory › Sources**). Add one source per camera image you use. Their
release pages:

- ESP32-P4-WIFI6 + OV5647: [releases](@@rel_cam_p4_wifi6_releases@@)
- ESP32-P4-Module + OV5647: [releases](@@rel_cam_p4_module_releases@@)
- BeagleY-AI SD card: [releases](@@rel_byai_sdcard_releases@@)

Open **Factory › Catalog** to check the images are listed. The catalog groups entries by the
name the devices report, and marks each name's active update target with ✓.

```{todo}
Name the GitHub repositories the camera images are published to (none are public yet), and
decide how BeagleY-AI images (`byai_sdcard`, `byai_system`, `byai_camera`) reach users' hubs:
today they are staged on the reference hub as a local source with `nn-stage-hub`.
```

## Then set up your camera

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} FreeRTOS camera: ESP32-P4
:link: esp32-p4
:link-type: doc

Flash over USB from the hub, then provision over Bluetooth.
:::

:::{grid-item-card} Linux camera: BeagleY-AI
:link: beagley-ai
:link-type: doc

Write a microSD card from the hub, boot, then provision over Bluetooth. Runs detection on the
camera itself, and can host a Thread gateway.
:::
::::

After that: {doc}`ota`.

```{toctree}
:hidden:

esp32-p4
beagley-ai
ota
```
