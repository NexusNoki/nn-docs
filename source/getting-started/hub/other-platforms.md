# Other hub platforms

The hub itself is a Python service with no special hardware needs beyond a Bluetooth radio, so it
is expected to run on any Linux machine. What differs between machines is mostly the **media
server**, which relies on a hardware video codec and an NPU.

These platforms are **planned**. Each section says what is known today.

## Mac mini

:::{todo}
Mac mini: decide between running the hub in a Linux VM or container and a native macOS service;
BlueZ is Linux-only, so native macOS needs a different Bluetooth backend. Document once tested.
:::

## x86 PC

- The hub installs exactly as on the Orange Pi ({doc}`orange-pi-6-plus`, steps 2 to 6).
- The media server has no CIX codec or NPU: detection runs on the CPU with an `.onnx` model.

:::{todo}
x86 PC: document the media server's software video decode path and expected CPU load per camera.
:::

## Raspberry Pi

- The hub installs as on the Orange Pi. Use the built-in Bluetooth or a USB adapter.
- A Raspberry Pi is better as a hub only, with the media server on a stronger machine.

:::{todo}
Raspberry Pi: test the hub on a Pi 5 and document the Bluetooth setup and any media server
limits.
:::
