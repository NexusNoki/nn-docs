# Firmware catalog

Every nn image is published on the **Releases** page of its public repository under
[@@github_owner@@](@@github_base@@). This page lists them all: what each image is for, which
board and sensor it needs, what a release contains, and how to install it.

## How releases work

- **One release, one tag.** All repositories are released together under the same tag (for
  example `v0.0.1`), and a submodule in one repository always points at the release commit of
  the same tag. Take every image of one tag, not a mix.
- **The image version is the tag.** Firmware built for `v0.0.1` reports version `0.0.1` to the
  hub.
- **Every release carries `SHA256SUMS` and `release.json`.** `release.json` names the source
  commit and lists every file with its size and SHA-256. Check a download before you flash it:

  ```console
  $ sha256sum -c --ignore-missing SHA256SUMS
  ```

- **Hub-ready releases** carry `image.signed.bin` + `manifest.json` (+ `flash.sh`): the hub's
  Factory can list them from a GitHub source (see {doc}`/getting-started/sensors/index`). The
  others are installed with the tools shown for each.

The newest release of a repository is always at `…/releases/latest`.

## Sensors and radios (ESP32-C6, Zephyr)

All three run on an **ESP32-C6-DevKitC-1** and ship `image.signed.bin` + `manifest.json`; the
sensor also ships `flash.sh`.

| Image | What it is | Install |
|---|---|---|
| [nn-app-mdns-ot-esp32c6](@@github_base@@/nn-app-mdns-ot-esp32c6/releases/latest) | The example **sensor**: button, LED, example readings, automations | hub-ready: Factory › Flash device, then over the air ({doc}`/getting-started/sensors/index`) |
| [nn-app-ncp-esp32c6](@@github_base@@/nn-app-ncp-esp32c6/releases/latest) | The **Thread radio** (NCP) of a gateway, on the USB port | Factory › Flash device (from `v0.0.2`) |
| [nn-app-ncp-host-esp32c6](@@github_base@@/nn-app-ncp-host-esp32c6/releases/latest) | Example gateway host on an ESP32-C6 (developers) | USB |

All three are MCUboot images: `image.signed.bin` goes to the application slot at `0x20000`. From
release `v0.0.2` on, the sensor and NCP releases also carry `flash.sh` and **`mcuboot.bin`** (the
bootloader), so Factory can bring up a blank board (**first flash**).

## Cameras

Each camera image is built for **one board and one image sensor**; see
{doc}`/getting-started/cameras/index` before you choose.

| Image | Board | Image sensor |
|---|---|---|
| [nn-app-camera-esp32p4-wifi6-sdio-ov5647](@@github_base@@/nn-app-camera-esp32p4-wifi6-sdio-ov5647/releases/latest) | Waveshare ESP32-P4-WIFI6 | OV5647 |
| [nn-app-camera-esp32p4module-sdio-ov5647](@@github_base@@/nn-app-camera-esp32p4module-sdio-ov5647/releases/latest) | Waveshare ESP32-P4-Module-DEV-KIT | OV5647 |
| [nn-app-camera-esp32wifi6-sdio-imx708](@@github_base@@/nn-app-camera-esp32wifi6-sdio-imx708/releases/latest) | ESP32-P4-WIFI6 (experimental) | IMX708 |
| [nn-app-camera-esp32p4module-sdio-imx708](@@github_base@@/nn-app-camera-esp32p4module-sdio-imx708/releases/latest) | ESP32-P4-Module-DEV-KIT (experimental) | IMX708 |
| [nn-app-media-network](@@github_base@@/nn-app-media-network/releases/latest) | the ESP32-C6 **network co-processor** on either P4 board | — |
| [nn-app-camera-beagleyai-imx708](@@github_base@@/nn-app-camera-beagleyai-imx708/releases/latest) | BeagleY-AI (Linux camera) | Camera Module 3 **Wide NoIR** |

The ESP32-P4 cameras and the co-processor are FreeRTOS images released as an **ESP-IDF set**;
the BeagleY-AI is a Linux camera released as a card image, a system image and an app bundle.

### ESP-IDF set (ESP32-P4 cameras, ESP32-C6 co-processor)

A release carries the whole flash: `bootloader.bin`, `partition-table.bin`,
`ota_data_initial.bin`, the application `<image>.bin`, and `flasher_args.json`, which gives the
chip, the flash settings and the address of each file. Write them all over USB with
[esptool](https://docs.espressif.com/projects/esptool/), using the values from
`flasher_args.json`. For the ESP32-P4-WIFI6 camera:

```console
$ esptool --chip esp32p4 -p /dev/ttyUSB0 -b 460800 --before default-reset --after hard-reset \
    write-flash --flash-mode dio --flash-size 16MB --flash-freq 80m \
    0x2000  bootloader.bin \
    0x8000  partition-table.bin \
    0xf000  ota_data_initial.bin \
    0x20000 nn-app-camera-esp32p4-wifi6-sdio-ov5647.bin
```

The ESP32-C6 co-processor image uses `--chip esp32c6`, `--flash-size 8MB`, and its bootloader at
`0x0`. Writing only the application (`0x20000`) keeps the settings and keys of a provisioned
camera; writing all four resets the board to factory state.

From release `v0.0.2` on, each ESP-IDF release also carries `image.signed.bin` (the application),
a `manifest.json` and a **self-contained `flash.sh`** (bootloader, partition table and otadata
embedded), so the hub's Factory can flash it from any source, blank board included.

### BeagleY-AI release

| File | What it is | Use |
|---|---|---|
| `byai_sdcard-<ver>.img.xz` | the complete microSD card | write it with Factory › Flash device, or any card writer ({doc}`/getting-started/cameras/beagley-ai`) |
| `byai_system-<ver>.rootfs.ext4.xz` | one system slot, for over-the-air system updates | used by the hub's system update ({doc}`/getting-started/cameras/ota`) |
| `byai_camera-<ver>.tar.gz` | the camera application bundle (`byai_camera.tar.gz` in `v0.0.1`) | used by the hub's app update |
| `*.manifest.json` | versions, sizes and checksums of the two images | read by the hub |

From release `v0.0.2` on the app bundle is `byai_camera-<ver>.tar.gz` with its own manifest, and
a hub GitHub source pointed at this repository lists all three images.

## Hub and gateway

| Image | What it is | Runs on | Release contents |
|---|---|---|---|
| [nn-hub](@@github_base@@/nn-hub/releases/latest) | The hub and the media server, each with its installer | the hub machine | `nn-hub-<ver>.tar.gz`, `nn-media-host-<ver>.tar.gz` |
| [nn-modules](@@github_base@@/nn-modules/releases/latest) | The Linux Thread gateway `gw_linux` | an arm64 Linux machine with an NCP radio (Debian 12 or newer) | `nn-gateway-linux-arm64-<ver>.tar.gz` (with `install-gateway.sh`), `gw_linux-arm64` |

See {doc}`/getting-started/hub/index`, {doc}`/getting-started/media-server` and
{doc}`/getting-started/gateway` for installing them.

## This manual

| Image | What it is | Release contents |
|---|---|---|
| [nn-docs](@@github_base@@/nn-docs/releases/latest) | This manual as a static website | `nn-docs-html-<ver>.tar.gz` |

## Source-only repositories

These have no images; they are the source the images are built from:
[nn-app-build](@@github_base@@/nn-app-build) (the firmware build kit),
[nn-platform](@@github_base@@/nn-platform), [nn-manifest](@@github_base@@/nn-manifest),
[nn-app-media](@@github_base@@/nn-app-media) (the shared FreeRTOS camera application) and
[nn-media-stream](@@github_base@@/nn-media-stream).
