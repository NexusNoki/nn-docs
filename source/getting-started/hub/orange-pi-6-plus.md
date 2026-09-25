# Hub on the Orange Pi 6 Plus

This page installs the hub on an Orange Pi 6 Plus. At the end, the nn web app is open in your
browser and the hub can see its Bluetooth radio.

:::{note}
nn does not ship an installer yet. The steps below are the ones the reference Orange Pi was set
up with; they will be replaced by a package.
:::

```{todo}
Replace this manual procedure with the nn installer or package once one exists, and document
how to update the hub (there is no documented update procedure yet).
```

## 1. Prepare the board

1. Fit the **Wi-Fi/Bluetooth antenna**. Without it the on-board Bluetooth radio hears almost
   nothing, and provisioning devices fails intermittently.

   :::{photo-needed} Orange Pi 6 Plus with the antenna fitted
   :id: opi6-antenna
   Top view of the Orange Pi 6 Plus showing where the antenna cable connects (the U.FL socket
   for Wi-Fi/Bluetooth), with the antenna attached. Label the socket.
   :::

2. Install the Orange Pi Debian 12 (bookworm) image on the board's storage and boot it.

   ```{todo}
   Name the exact Orange Pi 6 Plus OS image (version, download page) nn is tested with.
   ```

3. Log in, and give the board a fixed address in your router (this tutorial uses `@@hub_ip@@`).

## 2. Bluetooth and serial ports

The hub provisions devices over Bluetooth and flashes boards over USB serial. Three one-time
settings make both reliable:

```console
$ sudo usermod -aG bluetooth,dialout $USER      # use the radio and USB serial without sudo
$ sudo rfkill unblock bluetooth                  # the image ships with Bluetooth soft-blocked
$ sudo systemctl disable --now ModemManager      # it grabs ESP32 USB ports while you flash
```

Make the unblock survive reboots with a small unit:

```{code-block} ini
:caption: /etc/systemd/system/bt-unblock.service

[Unit]
Description=Unblock Bluetooth before BlueZ starts
Before=bluetooth.service

[Service]
Type=oneshot
ExecStart=/usr/sbin/rfkill unblock bluetooth

[Install]
WantedBy=multi-user.target
```

```console
$ sudo systemctl enable bt-unblock.service
```

Log out and back in so the group change takes effect, then check the radio:

```console
$ bluetoothctl list
Controller XX:XX:XX:XX:XX:XX orangepi6plus [default]
```

## 3. Install the hub software

The hub installs into its own Python environment under `/opt/nn-hub`.

```console
$ sudo apt install python3-venv python3-dev git
$ sudo mkdir -p /opt/nn-hub && sudo chown $USER /opt/nn-hub
$ git clone @@repo_hub_url@@.git ~/nn-hub
$ python3 -m venv --system-site-packages /opt/nn-hub/venv
$ /opt/nn-hub/venv/bin/pip install ~/nn-hub
$ /opt/nn-hub/venv/bin/nn-hub identity          # prints the hub's keys: the install works
```

:::{note}
The repository is private today. If `git clone` asks for credentials you have not been given
access yet; see {doc}`/reference/about-these-docs`.
:::

`--system-site-packages` lets the hub use the Debian-packaged system libraries (such as the
BlueZ bindings) alongside its own.

## 4. Run the hub as a service

```{code-block} ini
:caption: /etc/systemd/system/nn-hub.service

[Unit]
Description=nn hub
After=network-online.target bluetooth.service
Wants=network-online.target

[Service]
User=orangepi
WorkingDirectory=/opt/nn-hub
ExecStart=/opt/nn-hub/venv/bin/nn-hub serve --api-host 0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Replace `orangepi` with your user. If the board has more than one Bluetooth adapter (for example
a USB dongle beside the built-in one), pin the one to use:

```{code-block} ini
:caption: /etc/systemd/system/nn-hub.service.d/bleadapter.conf

[Service]
Environment=NN_BLE_ADAPTER=hci0
```

```console
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now nn-hub
$ systemctl status nn-hub --no-pager
```

## 5. Open the web app

Browse to **http://@@hub_ip@@:8769/devices**. You see the nn web app with an empty device list.

:::{photo-needed} The web app on first open
:id: webapp-first-open
Screenshot of the Devices page on a fresh hub (empty device list, sidebar visible).
:::

The hub keeps its data in `~/.nn-hub` of the user it runs as: the database, its keys, the
firmware catalog cache and the device logs. **Back this folder up** — the keys in it are what
your devices trust.

## 6. Optional: port 80 with a password

Out of the box the web app is on port 8769 with no login, which is fine on a trusted home
network. To serve it on port 80 behind a password, put nginx in front:

```console
$ sudo apt install nginx apache2-utils
$ sudo cp ~/nn-hub/deploy/nn-hub.nginx.conf /etc/nginx/sites-available/nn-hub
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
## 7. Optional: reach the web app from outside your home

To use the web app away from home, publish it through a **reverse proxy** that adds HTTPS and a
login, instead of opening ports on your router. A **Cloudflare Tunnel** is one way: a small agent
on the hub makes an outgoing connection to Cloudflare, so no port on your router is opened.

1. Set up the password-protected port 80 first (step 6).
2. Install `cloudflared` on the hub and create a tunnel in your Cloudflare account, following
   Cloudflare's own guide.
3. Point the tunnel's public hostname (for example `nnhub.example.com`) at
   **`http://localhost:80`**, the nginx site. Never point it at port 8769, which has no login.
4. Optionally add a Cloudflare Access policy, so only your own accounts reach the login page.

Then browse to **https://nnhub.example.com/devices**.

:::{note}
Only the web app goes through the tunnel. Cameras, gateways and sensors keep talking to the hub
on your home network, and keep working when the internet is down.
:::

```{todo}
Remote access: confirm which web app features need port 8769 directly (for example live video
or card writing) and whether they work through the tunnel; add the `cloudflared` config file
used on the reference hub, with its hostname made a docs variable.
```

## Check

- [ ] `systemctl status nn-hub` shows **active (running)**.
- [ ] `bluetoothctl list` shows a controller.
- [ ] The Devices page opens in your browser.

Next: {doc}`/getting-started/media-server`.
