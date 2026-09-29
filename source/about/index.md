# About nn

**nn** (short for **nexus-noki**) is a home system you run yourself: a hub, cameras and sensors
that work together on your own network, with no cloud service in the loop.

- The **hub** is a small Linux computer at home. It runs the web app, keeps the devices'
  records, sets new devices up over Bluetooth, and updates their firmware.
- **Cameras** stream to a media server on the same network, which records events and
  recognises people and objects on the device or on the hub's own AI accelerator.
- **Sensors** form a Thread mesh and run your automations themselves.

## Who it is for

- **Makers and hobbyists** who are happy to flash a board and follow a step-by-step guide.
- **Privacy-minded households** who want cameras and sensors without a subscription or a
  vendor's cloud.
- **Developers** who want to change the firmware, write their own device apps, or port nn to
  new boards.
- **Product builders**: the licence lets companies build and sell devices on nn.

## Licence

The source code is licensed under the **Apache License 2.0** and this manual under **Creative
Commons Attribution 4.0**. Each repository carries its `LICENSE`; parts that come from other
projects keep their own licences.

## Get involved

nn is young. The easiest way to follow it is to **watch the releases** of the
[NexusNoki repositories](@@github_base@@).

- **Issues and pull requests are welcome** on those repositories: bug reports, questions about
  this manual, fixes and new boards. {doc}`contribute` lists who can help and how.
- For open-ended questions and ideas, use the discussions.

```{todo}
Link the discussion place (GitHub Discussions on a NexusNoki repository, or a chat server) once it
is set up.
```

```{toctree}
:maxdepth: 1

philosophy
contribute
```
