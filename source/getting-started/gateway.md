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

```{todo}
Confirm that the NCP release ships a `flash.sh` so it appears in Factory › Flash device, and
whether a blank ESP32-C6 needs the bootloader flashed first (as sensors do). If not, document
the bench flashing command instead.
```

## 2. Gateway on the hub

The hub runs the gateway as a service called **nn-gw**. It finds the NCP by itself: it looks for
an Espressif USB device first, then the serial ports.

```{todo}
The hub's `nn-gw.service` and `gw-supervise` are not in a released package yet. Add the install
steps (binary, unit file, `/var/lib/nn-gw`), then the first-start command, here. The CI
gateway artifact is built for Debian 13 (trixie) only, so it does not install on the Orange Pi's
Debian 12 yet.
```

Start the service. On its first start the gateway has no identity yet, so it waits to be
provisioned on the local network (TCP port 8770):

```console
$ sudo systemctl enable --now nn-gw
```

Then provision it from the hub. This hands it the hub's address and the Thread network, and
registers it:

```console
$ /opt/nn-hub/venv/bin/nn-hub gateway new --transport net --addr 127.0.0.1:8770 \
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
