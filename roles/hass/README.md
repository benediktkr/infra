# hass

Home assistant setup. Inlcudes other roles in `meta/main.yaml`, for example:

 * `hass-zwave`: zwavejs for z-wave devices
 * `hass-nginx`: nginx reverse proxy config, including for zwavejs.
 * `hass-zigbee`


# notes

couple of reucurring problems, need to keep notes of them.


## occupancy notes

VOC and CO2 are useful, when occupied:

 * VOC > 0.25-0.30 ppm
 * CO2 > 550-600 ppm

Their derivatives however are supririsngly less useful.


## Monitor

Powered on, charging laptop with USB-C: 40-80W
Standby (monitor off) charging a laptop: 15-25W
Powered on, without charging laptop (laptop connected with hdma): 23W
Standby, without charging laptop: <2-W

Make state sensor based on timestamps and watt ranges.


Something like this:

```python

if timestamp(watts > 45) < timestamp(watts < 3):
  monitor.usb_c_power_state = "charging laptop"
else:
  monitor.usb_c_power_state = "off"

# inverted, not sure which i like better
if timestamp(watts < 3) < timestamp(watts > 45):
  monitor.usb_c_power_state = "off"
else:
  monitor.usb_c_power_state = "off"


if watts > 20:
  if monitor.usb_c_power_state_off:
    monitor.state = True
  else:
    monitor.state = False
else:
  monitor.state = False

```
