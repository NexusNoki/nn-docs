# Set up the sensors

The example sensor is an **ESP32-C6-DevKitC-1** running the nn sensor firmware. It needs no
extra wiring. It uses parts already on the board:

| Part on the board | nn field | What it does |
|---|---|---|
| **BOOT** button (GPIO 9) | `button` | each press toggles the value between 0 and 1 |
| RGB LED (GPIO 8) | `led` | lights green when set to 1 |

The firmware also reports example `temperature`, `humidity` and `light` values, and has a `fan`
output, so you can try rules without any sensors attached.

:::{photo-needed} The example sensor board
:id: sensor-c6-board
An ESP32-C6-DevKitC-1 from above, with the BOOT button and the RGB LED labelled, and the USB-C port
used for flashing marked.
:::

Before you start, you need a working gateway: {doc}`/getting-started/gateway`.

## 1. Add the firmware to the catalog

The hub keeps a **firmware catalog**: every image it can flash and update devices with. It fills
the catalog from **sources**, which are release pages it checks by itself.

1. Open **Factory › Sources**.
2. Under **Add a GitHub catalog**, fill in:
   - a **source name**, for example `nn-sensors`;
   - the repository **owner/repo**: **`@@github_owner@@/@@rel_sensor@@`**;
   - leave the **token env var** empty: the repository is public.
3. Press **Add**, then **Sync**.
4. Open **Factory › Catalog**. The sensor firmware **`@@rel_sensor@@`** is listed with its
   versions.

The releases are on the [sensor firmware releases page](@@rel_sensor_releases@@). Each release
(tagged like `v0.0.1`) carries the signed image, a `manifest.json` and a `flash.sh`. The hub
checks every source again every five minutes.

```{todo}
Flash and provision a sensor from a freshly installed hub on real hardware. Checked so far on a
clean Debian 12 install: the installer, adding the public source, the catalog listing v0.0.1 as
flashable, and downloading its flash script and verified image.
```

## 2. Flash the sensor

1. Plug the ESP32-C6 into the hub with a USB-C cable.
2. Open **Factory › Flash device**.
3. Pick **`@@rel_sensor@@`** and the board's port (**Rescan** if needed).
4. Press **Flash**.

The hub fetches the release's flash script from GitHub and writes the application; it keeps the
bootloader and the board's settings.

**First flash of a blank board.** A board that has never run nn firmware also needs its
bootloader: tick **first flash (blank chip)** before you press **Flash**. The hub then writes the
release's bootloader (`mcuboot.bin`) as well; the checkbox appears only for releases that carry
it. A re-flash leaves it unticked, which keeps the device's keys and Thread settings.

After flashing, the board has no network settings yet, so it advertises over Bluetooth in
**setup mode**. Unplug it from the hub and power it from any USB charger where you want it.

## 3. Provision and register

1. Open **Devices** and press **Add device**.
2. **What are you adding?** Choose **Sensor**.
3. **Find the device**: press **Scan**. Your board appears within ten seconds.
4. **Details**: give it a **Name**, for example `c6-s1`, keep the type `sample_c6`, and press
   **Start setup**.
5. **Register**: the hub sends the board the Thread network over Bluetooth. Wait for both lines
   to tick: *provisioning c6-s1* and *device joins the mesh*.

:::{photo-needed} The Add device wizard, sensor registered
:id: webapp-add-sensor
Screenshot of the Add device wizard's Register step with both checklist lines ticked.
:::

The sensor card then appears on **Devices**. Press the board's **BOOT** button: the card's
`button` value flips within a second or two.

:::{tip}
*Nothing in setup mode found*: a board that is already provisioned stops advertising. Unregister
it first. *No contact in 3 min — check the gateway*: the board could not reach a gateway. Check
the **Gateway** page shows one online.
:::

Repeat for two more boards, for example `c6-s2` and `c6-s3`, before you try automation.

```{toctree}
:hidden:

automation
ota
```

Next: {doc}`automation`.
