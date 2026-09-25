# Update cameras over the air

Cameras **pull** their updates. You set a target version on the hub, and each camera checks the
hub about every ten minutes, downloads the target, installs it, and then checks itself. If the
new version is not healthy, it goes back to the old one by itself.

## See what a camera runs

Open the camera, then **Device Status › Firmware**. The panel shows:

- **running**: the version and image name, and when the camera last reported;
- **target**: the version the camera should run. It *applies on the camera's next 10-min tick,
  self-confirms or rolls back*.

A BeagleY-AI camera also shows its **system** version, and which of its two system slots
(**a** or **b**) it booted from.

:::{photo-needed} The camera Firmware panel
:id: webapp-camera-firmware
Screenshot of a BeagleY-AI camera's Device Status › Firmware panel showing running, system slot
and target.
:::

## Update a camera

1. Make sure the new version is in **Factory › Catalog** (sources sync every five minutes, or
   press **Sync**).
2. In the camera's **Firmware** panel, choose the version and press **Set target**.
3. Wait. Within about ten minutes the camera downloads the version, restarts into it and
   confirms it. The panel's *running* line changes to the new version.

**Set target** promotes that version for **every camera with the same image**, not only this
one. Check **Factory › Fleet** to follow them: each shows *behind* until it has updated, then
*up to date*.

## BeagleY-AI: system updates and rollback

A BeagleY-AI card holds **two copies of the system** (slot a and slot b). An update is written
to the copy that is **not** running, so the running camera is never touched:

1. The camera downloads the new system from the hub into the idle slot and checks it.
2. It restarts into the new slot.
3. It checks itself: camera, network, the connection to the hub.
4. **Healthy**: it keeps the new slot. **Not healthy**, or it fails to start three times: it
   goes back to the old slot and does not try that version again.

A full update takes 5 to 10 minutes from **Set target** to confirmed. The camera app and its
container update the same way, but in place, without a second copy.

```{todo}
The Firmware panel's **Set target** only lists versions of the camera app (`byai_camera`), not
of the system image (`byai_system`). Document how users promote a system image from the web app
once that is possible (today: `nn-hub firmware promote byai_system <version>` on the hub).
```

## ESP32-P4 cameras

```{todo}
Confirm that an ESP32-P4 camera updates itself when a target is set: the board has two app
slots, but no update agent was found in the camera firmware. Document the steps once it is
verified on hardware, or say that ESP32-P4 cameras are updated over USB for now.
```

## Updating at a set time

Scheduling an update for later exists for sensors only (see {doc}`/getting-started/sensors/ota`).
Cameras update at their next check after you set the target.

Next: {doc}`/getting-started/gateway`.
