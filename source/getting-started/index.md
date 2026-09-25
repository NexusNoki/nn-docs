# Getting started

This tutorial takes you from nothing to a working nn home: a **hub** that runs everything, a
**media server** for your cameras, **cameras** that stream, record events and update themselves,
a **Thread gateway**, and **sensors** that talk to each other through automations.

Follow the pages in order. Each one ends with a check that tells you it worked before you move on.

```{mermaid}
flowchart LR
    subgraph home["Your home network"]
      HUB["Hub<br/>web app · catalog · provisioning · automations"]
      MS["Media server<br/>video · HLS · detection · events"]
      GW["Thread gateway<br/>border router"]
      PHONE["Browser / phone<br/>at home"]
    end
    CAM1["FreeRTOS camera<br/>e.g. ESP32-P4"] -- Wi-Fi --> MS
    CAM2["Linux camera<br/>e.g. BeagleY-AI"] -- Wi-Fi --> MS
    MS -- registers cameras --> HUB
    GW -- USB / LAN --> HUB
    S1["Sensor"] -. Thread mesh .- GW
    S2["Sensor"] -. Thread mesh .- GW
    S3["Sensor"] -. Thread mesh .- CAM2
    CAM2 -. "camera as gateway (optional)" .-> HUB
    PHONE -- LAN --> HUB
    AWAY["Browser / phone<br/>away from home"] -. HTTPS .-> RP["Reverse proxy<br/>e.g. Cloudflare Tunnel"]
    RP -. "tunnel (optional)" .-> HUB
```

At home you open the web app directly. To reach it from anywhere else, you can put a reverse
proxy in front of the hub, for example a Cloudflare Tunnel. This is optional; see
{ref}`remote-access`.

A Linux camera can also be a Thread gateway: plug an ESP32-C6 radio into it, and sensors near
the camera join the mesh through it. See {doc}`gateway`.

| Step | Page | You end with |
|---|---|---|
| 1 | {doc}`planning` | a list of what runs where, and the parts to buy |
| 2 | {doc}`hub/index` | the nn web app open in your browser |
| 3 | {doc}`media-server` | the media server healthy and known to the hub |
| 4 | {doc}`cameras/index` | a camera streaming live video in the web app |
| 5 | {doc}`cameras/ota` | a camera updated to a new firmware from the catalog |
| 6 | {doc}`gateway` | a Thread network with a border router |
| 7 | {doc}`sensors/index` | sensors registered and reporting |
| 8 | {doc}`sensors/automation` | a button on one sensor switching the others |
| 9 | {doc}`sensors/ota` | the sensors updated over the air |

:::{tip}
Everything in nn is managed from the hub's web app. You will use a terminal only to install the
hub and the media server; flashing, provisioning, automations and updates are all buttons.
:::

```{toctree}
:maxdepth: 2
:hidden:

planning
hub/index
media-server
cameras/index
cameras/ota
gateway
sensors/index
sensors/automation
sensors/ota
```
