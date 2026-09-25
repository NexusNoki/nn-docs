# Update sensors over the air

Sensors update **over the Thread mesh**: no cable, no visit. The hub sends the new firmware in
small blocks, the sensor stores it beside the running one, checks its signature, and only then
restarts into it. If the new image does not start, the bootloader keeps the old one.

## 1. Get the new version into the catalog

When a new sensor release is published on its [releases page](@@rel_sensor_releases@@), the hub picks it up at the
next sync (every few minutes), or straight away if you press **Sync** in **Factory › Sources**.

## 2. Make it the target

**Promote** the new version: this says "this is the version sensors of this type should run".
It does not update anything by itself. The target version has a ✓ in **Factory › Catalog**.

There is no promote button in the Catalog tab. Promote from the hub's command line:

```console
$ /opt/nn-hub/venv/bin/nn-hub firmware promote @@rel_sensor@@ <version>
```

```{todo}
Add a Promote control to Factory › Catalog (the API exists:
`POST /api/v1/firmware/catalog/<name>/<version>/promote`) and replace the command above.
```

## 3. See who is behind

Open **Factory › Fleet**. Each device shows its status:

| Status | Meaning |
|---|---|
| **up to date** | runs the target version |
| **behind** | runs an older version: an update is available |
| **ahead** | runs a newer version than the target (for example a test build) |
| **differs** | runs a build whose version cannot be compared with the target (for example a development build) |
| **no target** | no version of its firmware is promoted |
| **unknown** | the device has not reported its version yet |

:::{photo-needed} The Fleet table with a device behind
:id: webapp-fleet
Screenshot of Factory › Fleet with at least one sensor *behind* and one *up to date*.
:::

## 4. Update one sensor

1. Open the sensor, then **Device Status › Firmware**.
2. Choose the version and press **Download**. The panel shows *downloading N%*. Over Thread this
   takes a few minutes.
3. When it says *downloaded: … (armed, ready to apply)*, apply it. The sensor restarts in about
   half a second and comes back on the new version.

To update later, for example at night, press **Schedule…**, pick the time under **Apply at** and
press **Schedule**. The panel shows *scheduled OTA* until then, with **cancel**. At that time
the hub downloads the image if needed, applies it, and clears the schedule once the device runs
the new version.

:::{warning}
Do not promote a different version while sensors are still downloading. A sensor rejects an image
that is no longer the target, and has to start again.
:::

## 5. Update the whole fleet

**Factory › Fleet** can apply the target to every device that is *behind*.

```{todo}
Describe the Fleet page's apply-all control once its label is settled (API:
`POST /api/v1/ota/fleet/apply`), and add a screenshot.
```

Next: back to {doc}`/getting-started/index`, or read {doc}`/reference/glossary`.
