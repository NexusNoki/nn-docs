# Enable the media server

The media server receives your cameras' video. It produces the live view and the HLS stream the
web app plays, runs motion and object detection, and records events. One process,
**nnvideo**, serves every camera.

You can run it:

- **on the hub machine** (recommended, and what this tutorial does), or
- **on another machine** (partly supported today; see [below](#media-on-another-machine)).

## On the hub machine

These steps continue on the Orange Pi 6 Plus from {doc}`hub/orange-pi-6-plus`.

### 1. The detector model

Object detection runs in a small helper, **nn-inferd**. It loads one model:

- a **`.cix`** model runs on the Orange Pi 6 Plus NPU;
- an **`.onnx`** model runs on the CPU (works anywhere, slower).

The NPU model is **YOLOX-S** from the CIX AI Model Hub on ModelScope
(`cix/ai_model_hub_25_Q3`, under `models/ComputeVision/Object_Detection/onnx_yolox_s`). Put it in
your home folder as `~/models/yolox_s.cix` (or anywhere, and pass `--model` below).

### 2. Install the media server

Download the newest **`nn-media-host-<version>.tar.gz`** from the
[hub releases page](@@repo_hub_url@@/releases/latest), unpack it and run its installer. The hub
must be installed first: the media server runs on the hub's Python environment and uses the hub's
keys.

```console
$ tar -xzf nn-media-host-<version>.tar.gz
$ cd nn-media-host-<version>
$ sudo ./deploy/install-media.sh --user $USER
```

It installs the video and AI packages, the four media services (**nn-inferd**,
**nn-transcoded**, **nn-media-ctrl**, **nn-video-pipelines**) and starts them. It points the
camera control channel at the hub's keys, and keeps the memory the services share when you log
out. Running it again on a newer release is the update.

:::{note}
The installer ships from release `v0.0.2` on.
:::

### 3. Check it

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

You can run the video part of the media server on a second machine, for example a PC with a
stronger processor beside a small hub. The **camera control channel** (nn-media-ctrl) stays on
the hub: it works with the hub's private key, which never leaves the hub.

This works from release `v0.0.2` on. The examples use `hub.lan` for the hub and `media.lan` for
the media machine; use their addresses.

1. **On the media machine**, unpack both the hub and the media-host release, put the model in
   place, and install the video services, telling them where the hub is and how the hub reaches
   this machine:

   ```console
   $ tar -xzf nn-hub-<version>.tar.gz
   $ tar -xzf nn-media-host-<version>.tar.gz && cd nn-media-host-<version>
   $ sudo ./deploy/install-media.sh --user $USER \
         --hub-url http://hub.lan:8769 --public-url http://media.lan:8880 \
         --hub-package ../nn-hub-<version>
   ```

   `--hub-package` installs the hub's Python code the video services need, without a hub.

2. **On the hub**, run the media installer for the control channel only, and re-run the hub
   installer with the media machine's address, so the first camera already streams there:

   ```console
   $ cd nn-media-host-<version>
   $ sudo ./deploy/install-media.sh --user $USER --services nn-media-ctrl
   $ cd ../nn-hub-<version>
   $ sudo ./deploy/install-hub.sh --user $USER --media-url http://media.lan:8880
   ```

3. Set up cameras as usual ({doc}`cameras/index`). The wizard now gives each new camera the
   media machine's address for its video and the hub's for its control channel.

:::{note}
The two machines must reach each other on ports **8769** (hub) and **8880** (media server), and
the cameras must reach the media machine on its video port (8886).
:::

```{todo}
Walk the two-machine setup end to end on real hardware (it is built and unit-tested, not yet run
on two machines).
```

Next: {doc}`cameras/index`.
