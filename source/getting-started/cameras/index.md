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
| Waveshare ESP32-P4-Module-DEV-KIT | IMX708 | `@@rel_cam_p4_module_imx708@@` |
| Waveshare ESP32-P4-WIFI6 | IMX708 | `@@rel_cam_p4_wifi6_imx708@@` |

:::{note}
The BeagleY-AI image is made and tuned for the **Wide NoIR** Camera Module 3. From release
`v0.0.2` on, the other variants (standard, Wide, NoIR) also start, since they use the same IMX708
sensor, but the colour tuning assumes a module without an infrared filter, so their pictures may
show a colour cast.
:::

```{todo}
Test a standard and a Wide Camera Module 3 on the BeagleY-AI, and tune colour for the modules
with an infrared filter.
```

## Add camera images to the catalog

The hub reads firmware from **sources** (see {doc}`/getting-started/sensors/index` for how to add
a GitHub source in **Factory › Sources**). Add one source per camera image you use. Their
release pages:

- ESP32-P4-WIFI6 + OV5647: [releases](@@rel_cam_p4_wifi6_releases@@)
- ESP32-P4-Module + OV5647: [releases](@@rel_cam_p4_module_releases@@)
- BeagleY-AI: [releases](@@rel_byai_sdcard_releases@@), with the SD card image
  (`byai_sdcard-*.img.xz`), the A/B system image and the camera app bundle
- Experimental IMX708 cameras: [ESP32-P4-WIFI6](@@rel_cam_p4_wifi6_imx708_releases@@),
  [ESP32-P4-Module](@@rel_cam_p4_module_imx708_releases@@)

Every release also carries `release.json` and `SHA256SUMS`, so you can check a download.

Open **Factory › Catalog** to check the images are listed. The catalog groups entries by the
name the devices report, and marks each name's active update target with ✓.

A GitHub source pointed at the BeagleY-AI repository lists all three of its images from release
`v0.0.2` on: the card image (`byai_sdcard`), the system image (`byai_system`) and the camera app
(`byai_camera`). You can also write the card image with any SD-card tool.

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
