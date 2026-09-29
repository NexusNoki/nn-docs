# Enable the Thread gateway

nn sensors talk over **Thread**, a low-power mesh radio network. A **gateway** (a border router)
links that mesh to your home network and to the hub. You need at least one before you add
sensors, and you can run more than one: they share the same mesh.

| Where the gateway runs | Radio | Status |
|---|---|---|
| **On the hub**, with a USB radio | ESP32-C6 with the NCP firmware, on USB | supported, used in this tutorial |
| **On a Linux camera** (BeagleY-AI) | ESP32-C6 with the NCP firmware, on the camera's USB | supported |
| On another Linux machine | ESP32-C6 on USB or a header UART | planned |

The gateway software is the same everywhere: a Linux program that drives an ESP32-C6 **NCP**
(network co-processor), which is the actual Thread radio.

## 1. Flash the NCP radio

Use an **ESP32-C6-DevKitC-1** board. Its NCP firmware is in the catalog as
**`@@rel_ncp@@`** ([releases](@@rel_ncp_releases@@)).

:::{photo-needed} ESP32-C6 DevKitC as the NCP, plugged into the hub
:id: ncp-usb-hub
The ESP32-C6-DevKitC-1 connected to the Orange Pi 6 Plus. Show which of the board's two USB-C
ports is used (the one labelled "USB", the native USB Serial/JTAG port, not "UART").
:::

1. Plug the ESP32-C6 into the hub with a USB-C cable, using its **USB** port.
2. In the web app, open **Factory › Flash device**.
3. Pick the **`@@rel_ncp@@`** firmware and the ESP32-C6's port (**Rescan** if it does not show).
4. Press **Flash**.

**First flash of a blank board.** A board that has never run nn firmware also needs its
bootloader: tick **first flash (blank chip)** before you press **Flash**. The hub then writes the
release's bootloader (`mcuboot.bin`) as well; the checkbox appears only for releases that carry
it. A re-flash leaves it unticked, which keeps the device's keys and Thread settings.

The NCP release carries its flash script from release `v0.0.2` on.

## 2. Gateway on the hub

The hub runs the gateway as a service called **nn-gw**. It finds the NCP by itself: it looks for
an Espressif USB device first, then the serial ports.

Download the newest **`nn-gateway-linux-arm64-<version>.tar.gz`** from the
[nn-modules releases page](@@repo_modules_url@@/releases/latest) and install it. `--on-hub` tells
it the hub runs on this machine, so the gateway takes its provisioning on port **8771** (the hub
itself uses 8770):

```console
$ tar -xzf nn-gateway-linux-arm64-<version>.tar.gz
$ cd nn-gateway-linux-arm64-<version>
$ sudo ./install-gateway.sh --on-hub
```

The service starts at once. On its first start the gateway has no identity yet, so it waits to
be provisioned. Its settings are in `/etc/nn-gw.env`, its identity in `/root/.local/state/nn-gw`;
running the installer again on a newer release updates it and keeps both.

:::{note}
The gateway package ships from release `v0.0.2` on.
:::

Then provision it from the hub. This hands it the hub's address and the Thread network, and
registers it:

```console
$ /opt/nn-hub/venv/bin/nn-hub gateway new --transport net --addr 127.0.0.1:8771 \
      --name hub-gw --hub-host @@hub_ip@@ \
      --ssid "<your Wi-Fi name>" --psk "<your Wi-Fi password>"
```

The service notices the new identity and starts routing.

The first gateway you add also **creates your Thread network**: the hub picks a random network
key and identifiers, on channel 15 by default. Every gateway and sensor you add later joins
that same network.

### Check

Open **Gateway** in the web app.

- The **Gateways** table lists your gateway, runs on **this hub (USB)**, status **online**.
- Its **role** becomes **leader** (the first gateway) or **router** after a minute or two.
- **Hub gateway service** shows the service active and the NCP port.

:::{photo-needed} The Gateway page with the hub gateway online
:id: webapp-gateway
Screenshot of the Gateway page: the Gateways table with one gateway online and the Hub gateway
service panel below.
:::

:::{tip}
If you unplug and replug the radio, the service can hold on to the old port and stop routing.
The **link errors** line then says *stale port, restart to re-probe*. Press **Restart** twice
(the first press asks *Really restart?*). The mesh takes up to five minutes to form again.
:::

## 3. Gateway on a Linux camera (BeagleY-AI)

A Linux camera such as the BeagleY-AI (see {doc}`cameras/beagley-ai`) can host a gateway too. This puts a
second border router somewhere else in the house, which extends the mesh.

1. Flash an ESP32-C6 with the NCP firmware, as in step 1.
2. Plug it into one of the BeagleY-AI's USB ports.

   :::{photo-needed} NCP radio plugged into a BeagleY-AI camera
   :id: ncp-usb-byai
   The BeagleY-AI camera with the ESP32-C6 NCP plugged into a USB-A port with a short cable.
   :::

3. Wait a minute. The camera notices the radio by itself.
4. In the web app, open the camera, then **Device Status › Gateway**. It says *This camera can
   host the Thread gateway (NCP detected)*.
5. Turn the toggle **on**.

The camera then starts its gateway and adds it to the hub as **`<camera>-gw`**. You do not need
to set up the camera again: it received its gateway identity when you provisioned it. Turn the
toggle off to stop it.

:::{warning}
Sensors attach to whichever gateway they hear best. If you turn a camera gateway off, the
sensors that were using it take a few minutes to move to another gateway.
:::

## 4. The Thread channel

**Gateway › Thread channel** shows the channel the mesh uses. **Scan** measures the noise on every
channel. **Move to** moves the whole mesh (every gateway and sensor) to a quieter channel
together, after a short delay. Wi-Fi on 2.4 GHz overlaps Thread, so pick a channel away from your
Wi-Fi.

Next: {doc}`sensors/index`.
