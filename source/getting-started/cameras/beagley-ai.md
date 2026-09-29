# Linux camera (BeagleY-AI)

The BeagleY-AI camera is a **Linux camera**: it runs a small Linux system. It runs object
detection **on the camera itself**, on the board's AI accelerator, and sends the media server video plus what it detected. It updates
its whole system safely over the air, and can host a Thread {doc}`gateway </getting-started/gateway>`.

## What you need

| Part | Notes |
|---|---|
| **BeagleY-AI** | with a 5 V / 3 A USB-C power supply |
| **Raspberry Pi Camera Module 3 Wide NoIR** (IMX708) | the only Camera Module 3 variant the image supports today: see {doc}`index` |
| **22-to-15-pin camera cable** | the "Standard-Mini" cable sold for the Raspberry Pi 5 |
| **microSD card**, 16 GB or larger | |
| **USB microSD card reader**, plugged into the hub | the hub writes the card |

## 1. Connect the camera module

Power off the board. The BeagleY-AI has two 22-pin camera connectors, **CSI0** and
**CSI1/DSI0**; the nn image uses **CSI0** (the camera-only one). Connect the camera module to
CSI0 with the 22-to-15-pin cable: the wide end goes into the board, the 15-pin end into the
camera. Insert the cable fully and evenly and close both latches.

:::{photo-needed} Camera Module 3 connected to the BeagleY-AI
:id: byai-csi-ribbon
Close-up of the BeagleY-AI's CSI connector with the ribbon inserted: which connector (the board
has two), which side the contacts face, the latch closed.
:::

```{todo}
Write the ribbon orientation in words from a photo of a working camera (the BeagleBoard docs
show the connectors only in diagrams).
```

## 2. Write the microSD card from the hub

1. Plug the card reader, with the card in it, into the hub.
2. Open the web app through an address the hub trusts for writing cards: your Cloudflare
   Tunnel address, the nginx site on port 80, or `http://localhost:8769` on the hub itself (see
   {doc}`/getting-started/hub/orange-pi-6-plus`). Writing cards is refused on the open
   port 8769 from another computer.
3. Open **Factory › Flash device**, and pick the **`@@rel_byai_sdcard@@`** image
   (`sdcard.img.xz`). The page changes to card mode and lists the card readers.
4. Pick the card reader. Type **ERASE** in the confirm box.
5. Press **Erase card & write**. The hub writes the card, then reads it back to check it.

When it says *card written and verified*, take the card out of the reader.

:::{photo-needed} The card reader plugged into the hub
:id: hub-card-reader
The Orange Pi 6 Plus with a USB microSD reader plugged in and a card in it.
:::

:::{warning}
Everything on the card is erased. The hub only lists removable card readers, never its own
disks, but check you picked the right reader.
:::

If the hub says it is missing **nn-sdflash**, the card-writing helper is not installed: run the
hub installer again ({doc}`/getting-started/hub/orange-pi-6-plus`, step 2); it installs it.

## 3. Boot the camera

Put the card in the BeagleY-AI and power it on. On the first boot it prepares the card, then
starts in **setup mode** and advertises over Bluetooth. This takes a minute or two.

## 4. Provision and register

The wizard is the same as for an ESP32-P4 camera ({doc}`esp32-p4`, step 3):

1. **Devices › + Add new device**. Choose **Wi-Fi camera**: BeagleY-AI cameras use the same
   Bluetooth setup.
2. In the scan result the camera shows as **Linux camera (BeagleY)**.
3. Give it a name, your Wi-Fi network and password, and press **Start setup**.
4. Wait for *camera joins Wi-Fi and registers*.

The camera then appears on **Devices**, and its detections appear on the **Events** tab.

:::{note}
The BeagleY-AI image has no SSH login and no default password: nobody can log into your camera
over the network. You manage it from the hub.
:::

## Unregister

As for ESP32-P4 cameras: **Device Status › Unregister device**. The camera wipes its settings
and returns to setup mode.

Next: {doc}`ota`.
