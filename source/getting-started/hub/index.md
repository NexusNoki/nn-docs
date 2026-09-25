# Install the hub

The hub is the heart of nn. It serves the web app you use for everything else, keeps the device
database and the firmware catalog, provisions new devices over Bluetooth, runs automations and
delivers over-the-air updates.

Pick your machine:

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Orange Pi 6 Plus
:link: orange-pi-6-plus
:link-type: doc

**Supported.** The reference machine: hub and media server on one board, with hardware video
and an NPU.
:::

:::{grid-item-card} Mac mini · x86 PC · Raspberry Pi
:link: other-platforms
:link-type: doc

**Planned.** What will differ, and what to watch for if you try it now.
:::
::::

## What every hub needs

- **Linux** with systemd. Debian 12 (bookworm) is what nn is tested on.
- **Python 3.10 or newer.**
- **A Bluetooth Low Energy adapter** that BlueZ can use (BlueZ 5.66 or newer recommended).
- **A fixed address** on your network.

```{toctree}
:hidden:

orange-pi-6-plus
other-platforms
```
