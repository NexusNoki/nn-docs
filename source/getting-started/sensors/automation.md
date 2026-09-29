# Automations

An automation is a rule: **when** a field on one device crosses a value, **set** fields on
other devices. nn compiles your rules and pushes them to the devices. The sensors then run them
**themselves, over the mesh**. A button press lights a lamp in another room without the hub
being in the loop, and the rules survive a device reboot.

This page builds the classic demo: press the button on `c6-s1`, and the LEDs on all three
sensors light up. Press it again, and they turn off.

## 1. Write the rule

Open **Automation › Modify rules**. You can build rules with the **Helper** on the left, or
write them directly in the editor on the right. The editor is `automations.yaml`, which is what
actually runs on the fleet.

Paste this in the editor:

```yaml
automations:
  - id: s1_btn_all_leds
    trigger:
      - device: c6-s1
        field: button
        above: 0.5
    action:
      - device: c6-s1
        field: led
        value: 1
      - device: c6-s2
        field: led
        value: 1
      - device: c6-s3
        field: led
        value: 1

  - id: s1_btn_all_leds_off
    trigger:
      - device: c6-s1
        field: button
        below: 0.5
    action:
      - device: c6-s1
        field: led
        value: 0
      - device: c6-s2
        field: led
        value: 0
      - device: c6-s3
        field: led
        value: 0
```

A trigger condition is one of `above`, `below`, `equals` or `not_equals`.

To use the **Helper** instead, fill in the rule id, the trigger device, field, condition and
threshold, add each action with **+ action**, and press **Add rule to editor**.

## 2. Compile and push

1. Press **Save & Compile**. The hub checks the rules and makes a small program for each device
   involved. The **Console** under the editor shows the result.
2. Press **Push to devices**. Each device confirms it received its rules.
3. Open **On devices**. Every device shows the same **rules version** and **compiled** time.

:::{photo-needed} Automation page after a push
:id: webapp-automation
Screenshot of Automation › Modify rules with the rule in the editor and the Console showing a
successful push, and a second one of the On devices table.
:::

## 3. Try it

Press **BOOT** on `c6-s1`. All three LEDs turn green. Press it again, and they turn off.

:::{photo-needed} Three sensors lighting together
:id: demo-leds-on
Photo (or a short video) of three ESP32-C6 boards on a desk with their LEDs lit after one button
press.
:::

On the **Devices** page each card follows along. A card shows *turning on…* while the hub waits
for a device to confirm, then the new value.

## The failsafe

Radio messages on a mesh can be lost. The hub watches for that: when a rule fired but a device
it should have changed did not report the new value within a few seconds, the hub sets that
value itself, with retries. It is on by default, with a 3-second delay.

There is no switch for it in the web app yet. You can read and change it through the API:

```console
$ curl http://@@hub_ip@@:8769/api/v1/auto/failsafe
$ curl -X PUT -H 'Content-Type: application/json' -d '{"enabled": true, "delay_s": 3}' \
      http://@@hub_ip@@:8769/api/v1/auto/failsafe
```

Next: {doc}`ota`.
