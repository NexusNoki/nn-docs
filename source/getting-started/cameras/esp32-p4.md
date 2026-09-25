# FreeRTOS camera (ESP32-P4)

The ESP32-P4 camera is a **FreeRTOS camera**: a small Wi-Fi camera whose firmware runs on
FreeRTOS (ESP-IDF) rather than Linux. The ESP32-P4 captures and encodes H.264 video, and an
ESP32-C6 beside it provides Wi-Fi and Bluetooth. Detection runs on the media server.

## What you need

| Part | Notes |
|---|---|
| **Waveshare ESP32-P4-WIFI6** *or* **Waveshare ESP32-P4-Module-DEV-KIT** | the ESP32-C6 radio is on the board |
| **OV5647 camera module** (Raspberry Pi Camera v1.3 class) with its ribbon cable | must be the OV5647: see {doc}`index` |
| USB-C cable | to flash it from the hub, and to power it later |

## 1. Connect the camera module

Power off the board. Open the camera connector's latch, insert the ribbon cable with the metal
contacts facing the right way, and close the latch.

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
Write the ribbon orientation in words for each board (for example "contacts toward the
board"), and say whether the OV5647 module needs the 22-pin or the 15-pin cable.
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

```{todo}
The camera images do not ship a `flash.sh` yet, so they cannot be flashed from Factory › Flash
device. Add one to each camera release (bootloader, partition table, app, and the ESP32-C6
radio firmware), then check these steps on a fresh board.
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
