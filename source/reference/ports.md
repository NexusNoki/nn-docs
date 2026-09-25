# Network ports

Every nn service listens on your local network only. None of them needs to be reachable from the
internet, and none should be forwarded from your router. To use the web app away from home, go
through a reverse proxy with a login instead (see {ref}`remote-access`).

## Hub

| Port | Protocol | Used by | What for |
|---|---|---|---|
| 80 | HTTP | browsers | the web app through nginx, with a password (optional) |
| 8765 | WebSocket | gateways | gateway connection to the hub |
| 8767 | TCP | cameras, gateways | nn device protocol (encrypted) |
| 8769 | HTTP | browsers, devices | REST API and the web app (`/devices`), **no login** |
| 8770 | HTTP | devices | firmware downloads for over-the-air updates |
| 5514 | UDP | devices | device logs (syslog) |

## Media server

| Port | Protocol | Used by | What for |
|---|---|---|---|
| 8880 | HTTP | the hub | media server API and health (`/health`) |
| 8886 | TCP | cameras | camera video in |
| 8888, 8890, 8892, 8894 | TCP | older cameras | legacy per-camera video ports, same service |
| 8772 | TCP | the hub | camera control (nn-media-ctrl) |
| 5700 | TCP | local only | transcoder, never leaves the machine |

:::{warning}
Port 8769 has no authentication. Keep the hub on a network you trust, and put nginx with a
password in front of it for browsers (see {doc}`/getting-started/hub/orange-pi-6-plus`).
:::
