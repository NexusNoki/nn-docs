# Enable the media server

The media server receives your cameras' video. It produces the live view and the HLS stream the
web app plays, runs motion and object detection, and records events. One process,
**nnvideo**, serves every camera.

You can run it:

- **on the hub machine** (recommended, and what this tutorial does), or
- **on another machine** (partly supported today; see [below](#media-on-another-machine)).

## On the hub machine

These steps continue on the Orange Pi 6 Plus from {doc}`hub/orange-pi-6-plus`.

### 1. System packages

```console
$ sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad python3-gi ffmpeg \
      python3-av python3-scipy python3-aiohttp python3-cryptography python3-pil \
      python3-numpy python3-opencv
$ /opt/nn-hub/venv/bin/pip install aiortc onnxruntime
```

### 2. The detector model

Object detection runs in a small helper, **nn-inferd**. It loads one model:

- a **`.cix`** model runs on the Orange Pi 6 Plus NPU;
- an **`.onnx`** model runs on the CPU (works anywhere, slower).

Put the model in your home folder, for example `~/models/yolox_s.cix`.

```{todo}
Say where users download the YOLOX-S `.cix` model (catalog release or a model page), and
document how to build `/opt/nn-accel/gen/nn_accel_pb2.py`, which the media services need
(`NN_ACCEL_GEN=/opt/nn-accel/gen`); its install step is not written down yet.
```

### 3. Install the services

The service files live in the hub repository under `media-host/units/`. Install them and point
them at your model:

```console
$ cd ~/nn-hub/media-host/units
$ sudo cp nn-inferd.service nn-transcoded.service nn-media-ctrl.service \
      nn-video-pipelines.service /etc/systemd/system/
$ sudo systemctl edit nn-inferd      # set --model to your model file if it differs
```

The media services share memory with each other, which systemd removes when the user logs out
unless you keep it:

```console
$ sudo mkdir -p /etc/systemd/logind.conf.d
$ printf '[Login]\nRemoveIPC=no\n' | sudo tee /etc/systemd/logind.conf.d/10-keep-service-shm.conf
$ sudo loginctl enable-linger $USER
```

**nn-media-ctrl** talks to cameras with the hub's key, so it must read the hub's data folder. On
the hub machine that is `~/.nn-hub`, the default.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now nn-inferd nn-transcoded nn-media-ctrl nn-video-pipelines
```

```{todo}
Verify the unit file names and the install list against `media-host/units/` in the release the
users get, and replace `cp` with the installer once one exists.
```

### 4. Check it

```console
$ curl http://localhost:8880/health
{"ok": true, ...}
```

In the web app, open **Pipelines**: it lists the media server with no cameras yet. Cameras appear
there by themselves once you set them up in {doc}`cameras/index`.

:::{photo-needed} The Pipelines page with the media server online
:id: webapp-pipelines-empty
Screenshot of the Pipelines tab showing the media host online and no cameras.
:::

(media-on-another-machine)=
## On another machine

Running the media server on a second machine (for example an x86 PC with a GPU, beside a small
hub) is a goal, but **not fully supported yet**. Today:

- the media server announces its streams with local addresses, which the hub cannot reach from
  another machine;
- the camera setup wizard tells cameras to send video to the **hub's** address;
- nn-media-ctrl needs a copy of the hub's key;
- each camera's hub address is a per-pipeline setting you have to change by hand.

```{todo}
Remote media server: make the media host register reachable stream URLs, let the setup wizard
send the media host's address to cameras, and define how the media host gets the key it needs
without copying the hub's private key. Then write this section as steps.
```

Until then, keep the media server on the hub machine.

Next: {doc}`cameras/index`.
