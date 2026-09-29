# Hub on the Orange Pi 6 Plus

This page installs the hub on an Orange Pi 6 Plus. At the end, the nn web app is open in your
browser and the hub can see its Bluetooth radio.



## 1. Prepare the board

1. Fit the **Wi-Fi/Bluetooth antenna**. Without it the on-board Bluetooth radio hears almost
   nothing, and provisioning devices fails intermittently.

   :::{photo-needed} Orange Pi 6 Plus with the antenna fitted
   :id: opi6-antenna
   Top view of the Orange Pi 6 Plus showing where the antenna cable connects (the U.FL socket
   for Wi-Fi/Bluetooth), with the antenna attached. Label the socket.
   :::

2. Download the official **Debian 12 (bookworm)** image. On the
   [Orange Pi 6 Plus download page](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-Pi-6-Plus.html),
   open **Official Images › Debian Image** and take the **Linux 6.6** build, with its `.sha`
   file:

   ```text
   Orangepi6plus_1.0.2_debian_bookworm_desktop_gnome_linux6.6.89.img.xz
   ```

   This is what the reference hub runs (Orange Pi OS 1.0.2, kernel 6.6.89). Take the 6.6 build
   rather than the 6.1 one beside it: the NPU and video drivers nn uses are tested on 6.6.

3. Check the download against its `.sha` file, then write it to the drive the board boots from.
   The reference hub boots from an **NVMe SSD** (write it with a USB-to-NVMe adapter); a
   microSD card of 32 GB or more works too, but is slower. Any image writer works, for example
   [balenaEtcher](https://etcher.balena.io/), or on Linux:

   ```console
   $ sha256sum -c Orangepi6plus_1.0.2_debian_bookworm_desktop_gnome_linux6.6.89.img.xz.sha
   $ xz -dc Orangepi6plus_1.0.2_debian_bookworm_desktop_gnome_linux6.6.89.img.xz \
         | sudo dd of=/dev/sdX bs=4M conv=fsync status=progress     # sdX = the SSD or card
   ```

4. Fit the drive, connect Ethernet and power (the board's USB-C PD supply), and boot. Log in as
   `orangepi` (the image's default password is `orangepi`) and **change the password** with
   `passwd` straight away.

5. Update the system, then give the board a fixed address in your router (this tutorial uses
   `@@hub_ip@@`):

   ```console
   $ sudo apt update && sudo apt full-upgrade
   ```

For anything board-specific (BIOS updates, booting from other media), the **User Manual** on the
same download page is the reference.

## 2. Install the hub

Download the newest **`nn-hub-<version>.tar.gz`** from the
[hub releases page](@@repo_hub_url@@/releases/latest) onto the board, unpack it and run its
installer as your own user (`orangepi` on the Orange Pi image):

```console
$ tar -xzf nn-hub-<version>.tar.gz
$ cd nn-hub-<version>
$ sudo ./deploy/install-hub.sh --user $USER
```

The installer:

- installs the hub into its own Python environment under `/opt/nn-hub`;
- lets your user use the Bluetooth radio and USB serial ports, unblocks Bluetooth at every boot,
  and turns off ModemManager (it grabs ESP32 boards' USB ports while you flash them);
- installs and starts the **nn-hub** service;
- installs the small helper Factory uses to write SD cards.

If the board has more than one Bluetooth adapter (for example a USB dongle beside the built-in
one), add `--ble-adapter hci0` (or `hci1`) to pick the one to use.

:::{note}
The installer ships with the hub releases from `v0.0.2` on. With an older release, follow the
manual steps in its README.
:::

Log out and back in once, so the new groups apply, then check:

```console
$ bluetoothctl list
Controller XX:XX:XX:XX:XX:XX orangepi6plus [default]
$ systemctl status nn-hub --no-pager
```

## 3. Updating the hub

Download a newer release and run its installer again, exactly as above. It reinstalls the hub
and restarts the service; your data in `~/.nn-hub` (devices, keys, firmware catalog, logs) is
not touched. Back that folder up before a big update all the same.

## 4. Open the web app

Browse to **http://@@hub_ip@@:8769/devices**. You see the nn web app with an empty device list.

:::{photo-needed} The web app on first open
:id: webapp-first-open
Screenshot of the Devices page on a fresh hub (empty device list, sidebar visible).
:::

The hub keeps its data in `~/.nn-hub` of the user it runs as: the database, its keys, the
firmware catalog cache and the device logs. **Back this folder up** — the keys in it are what
your devices trust.

## 5. Optional: a password on your home network

Out of the box the web app is on port 8769 with no login, which is fine on a trusted home
network. To require a password inside your home as well, serve it on port 80 through nginx
(not needed for remote access: step 6 has its own login):

```console
$ sudo apt install nginx apache2-utils
$ sudo cp nn-hub-<version>/deploy/nn-hub.nginx.conf /etc/nginx/sites-available/nn-hub
$ sudo ln -s /etc/nginx/sites-available/nn-hub /etc/nginx/sites-enabled/nn-hub
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo htpasswd -c /etc/nginx/nn.htpasswd <user>
$ printf 'auth_basic "nn";\nauth_basic_user_file /etc/nginx/nn.htpasswd;\n' | sudo tee /etc/nginx/nn-auth.conf
$ sudo nginx -t && sudo systemctl reload nginx
```

Then browse to **http://@@hub_ip@@/**.

:::{warning}
Port 8769 stays reachable on your network after this, without a password: cameras and gateways
use it. Never forward port 8769 (or any nn port) from your router to the internet.
:::

(remote-access)=
## 6. Optional: reach the web app from outside your home

To use the web app away from home, publish it through **Cloudflare Tunnel** and put
**Cloudflare Access** in front of it. The `cloudflared` agent on the hub makes an outgoing
connection to Cloudflare, so no port on your router is opened, and Access asks for a login
before any request reaches the hub. This is how the reference hub is reached.

You need a Cloudflare account with a domain on it (the examples use `nnhub.example.com`).

**Create the tunnel** (Cloudflare dashboard):

1. Go to **Networking › Tunnels** and select **Create a tunnel**. Name it, for example `nn-hub`.
2. Choose **Debian** and **arm64**. The dashboard shows an install command with your tunnel's
   token. Run it on the hub; it installs `cloudflared` and starts it as a service. It looks
   like this (copy yours from the dashboard, the token is secret):

   ```console
   $ sudo cloudflared service install <TOKEN>
   ```

3. In the tunnel's **Routes** tab select **Add route › Published application**: subdomain
   `nnhub`, your domain, and **Service URL** `http://localhost:8769`.

**Require a login** (Cloudflare Zero Trust dashboard):

4. Go to **Access controls › Applications › Create new application › Self-hosted and private**,
   and **Add public hostname** `nnhub.example.com`.
5. Add a policy: **Allow**, **Include** → **Emails**, with your own email addresses. Pick a
   session duration and **Create**.

Browse to **https://nnhub.example.com/devices**: Cloudflare asks you to log in, then the web app
opens. Everything works through the tunnel, including live video (the hub relays it) and
writing SD cards (the tunnel reaches the hub from the hub itself, which Factory trusts).

:::{warning}
Never route the tunnel to the hub without the Access application: port 8769 has no login of its
own. And never forward any nn port on your router.
:::

:::{note}
Only the web app goes through the tunnel. Cameras, gateways and sensors keep talking to the hub
on your home network, and keep working when the internet is down.
:::

## Check

- [ ] `systemctl status nn-hub` shows **active (running)**.
- [ ] `bluetoothctl list` shows a controller.
- [ ] The Devices page opens in your browser.

Next: {doc}`/getting-started/media-server`.
