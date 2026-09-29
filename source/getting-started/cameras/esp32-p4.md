# FreeRTOS camera (ESP32-P4)

The ESP32-P4 camera is a **FreeRTOS camera**: a small Wi-Fi camera whose firmware runs on
FreeRTOS (ESP-IDF) rather than Linux. The ESP32-P4 captures and encodes H.264 video, and an
ESP32-C6 beside it provides Wi-Fi and Bluetooth. Detection runs on the media server.

## What you need

| Part | Notes |
|---|---|
| **Waveshare ESP32-P4-WIFI6** *or* **Waveshare ESP32-P4-Module-DEV-KIT** | the ESP32-C6 radio is on the board |
| **OV5647 camera module** (Raspberry Pi Camera v1.3 class, 15-pin) | must be the OV5647: see {doc}`index` |
| **camera cable** | ESP32-P4-WIFI6: a **22-to-15-pin** cable (sold as the Raspberry Pi *Zero* camera cable); ESP32-P4-Module-DEV-KIT: a straight **15-pin** cable (in the kit) |
| USB-C cable | to flash it from the hub, and to power it later |

## 1. Connect the camera module

Power off the board. The two boards have different camera connectors:

| Board | Camera connector on the board | Cable for the 15-pin OV5647 module |
|---|---|---|
| ESP32-P4-WIFI6 | 22-pin, 0.5 mm (Raspberry Pi 5 style) | 22-to-15-pin ("Pi Zero camera cable") |
| ESP32-P4-Module-DEV-KIT | 15-pin (Raspberry Pi v1 style) | straight 15-to-15 |

Open the connector's latch, insert the cable fully and evenly, and close the latch. A ribbon that
is not seated straight often still lets the board find the camera but gives no picture.

:::{photo-needed} OV5647 ribbon cable in the ESP32-P4-WIFI6
:id: p4-wifi6-ribbon
Close-up of the ESP32-P4-WIFI6's MIPI-CSI connector with the OV5647 ribbon inserted: which
side the contacts face, and the latch closed. Label the connector.
:::

:::{photo-needed} OV5647 ribbon cable in the ESP32-P4-Module-DEV-KIT
:id: p4-module-ribbon
The same for the ESP32-P4-Module-DEV-KIT: the connector, the ribbon orientation, the latch.
:::

```{todo}
Write the ribbon orientation in words for each board (which side the metal contacts face),
from a photo of a working camera: Waveshare's pages show it only in pictures.
```

## 2. Flash it from the hub

1. Plug the board into the hub with a USB-C cable.

   :::{photo-needed} Which USB-C port to use on each ESP32-P4 board
   :id: p4-usb-port
   Both boards from above with the USB-C port used for flashing circled. On the ESP32-P4-WIFI6
   it is the **UART** port (the USB-to-serial chip), not the P4's own USB port.
   :::

2. Open **Factory › Flash device**.
3. Pick the image for your board (see {doc}`index`) and the board's port. Press **Rescan** if it
   does not show. Ports the gateway uses are locked and marked *never flash this*.
4. Press **Flash**, and wait for it to finish.

The camera releases carry a flash script from release `v0.0.2` on. It writes the whole flash
(bootloader, partition table and application), so it brings up a blank board as well; the
camera's settings and keys are outside those regions and survive a re-flash.

```{todo}
Walk these steps on a factory-blank ESP32-P4 board, and document flashing the ESP32-C6
co-processor (its own release, nn-app-media-network) when it needs an update.
```

After flashing, the camera has no Wi-Fi settings, so it starts in **setup mode** and advertises
over Bluetooth. Unplug it and power it where you want to mount it.

## 3. Provision and register

1. Open **Devices** and press **+ Add new device**.
2. **What are you adding?** Choose **Wi-Fi camera** (*ESP32 · BLE setup*).
3. **Find the device**: the scan starts by itself. Your camera appears within ten seconds.
4. **Details**:
   - **Name**: for example `Front door`.
   - **Wi-Fi network** and **Wi-Fi password**: the 2.4 GHz network the camera will use. The hub
     fills in everything else (the stream address and the keys).
   - **Camera slot**: keep *new camera*, unless you are replacing a camera you unregistered.
5. Press **Start setup**.
6. **Register**: wait for *provisioning Front door* and *camera joins Wi-Fi and registers*.

The camera restarts, turns its Bluetooth off, joins your Wi-Fi and registers. It then appears on
**Devices** and in **Pipelines**, and its live view starts.

:::{photo-needed} A newly registered camera
:id: webapp-camera-live
Screenshot of the camera's page right after registering, with the live view playing.
:::

:::{tip}
*No registration in 3 min — a wrong Wi-Fi password is the usual cause.* Unregister the camera
(see below) and run the wizard again.
:::

## Unregister or move a camera

On the camera's **Device Status** tab, **Unregister device** resets the camera. It wipes its
settings, and its records move to the archive. After 30 to 60 seconds it is back in setup mode.
Use **Force archive** only when the camera is unreachable.

Next: {doc}`ota`.
