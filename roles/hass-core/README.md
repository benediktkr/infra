# hass

[![Home Assistant logo](home-assistant.svg)](https://design.home-assistant.io/#brand/logo)

Documentation: [`www.sudo.is/docs/hass`](https://www.sudo.is/docs/hass)

# Current issues

## `sensor.rest_sensor`

```
homeassistant.exceptions.InvalidStateError: Invalid state with length 9656. State max length is 255 characters.
2023-11-05 16:13:49.067 ERROR (MainThread) [homeassistant.helpers.entity] Failed to set state for sensor.rest_sensor, fall back to unknown
```

what is `sensor.rest_sensor`, where is it coming from and how can i remove it?

fixed, see ops/meta#52

## Unsupported operands

```
2023-11-06 01:50:41.359 ERROR (MainThread) [homeassistant] Error doing job: Future exception was never retrieved
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/components/prometheus/__init__.py", line 184, in handle_state_changed_event
    self.handle_state(state)
  File "/usr/src/homeassistant/homeassistant/components/prometheus/__init__.py", line 197, in handle_state
    getattr(self, handler)(state)
  File "/usr/src/homeassistant/homeassistant/components/prometheus/__init__.py", line 438, in _handle_light
    value = state.attributes["brightness"] / 255.0
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
TypeError: unsupported operand type(s) for /: 'NoneType' and 'float'
```

pramming in jinja inside of a yaml document... should start on a custom integration + appdaemon.

## Removed

 * UI Lovelace Minimalist
 * browser-mod
 * forked-daapd-card
 * button-card
 * iphonedetect

```
# ls -1 /srv/hass/DISABLED/
browser_mod.storage
forked-daapd-card
```

see also: ops/meta#52

### UI Lovelace Minimalist

HACS integration: UI Lovelace Minimalist: https://github.com/UI-Lovelace-Minimalist/UI

```
# ls /srv/hass/config/ui_lovelace_minimalist/
custom_actions  custom_cards  dashboard
# ls /srv/hass/config/custom_components/ui_lovelace_minimalist/
base.py     config_flow.py  __init__.py    __pycache__    __ui_minimalist__
blueprints  const.py        lovelace       services.yaml  utils
cards       enums.py        manifest.json  translations
```

HACS wouldnt let me remove it ("The UI Lovelace Minimalist integration is configured or ignored, you need to delete the configuration for it before removing it from HACS "),

Integrationn was disabled, removed it from the integration page

Then i could remove it from the HACS integrations.

### browser_mod

this file may have been causing issues, removed browser mod a long time ago

```
# mv /srv/hass/home-assistantconfig/.storage/browser_mod.storage  ../DISABLED/
```

### forked-daapd-card

some ad-hoc one off install

```
# mv /srv/hass/home-assistant/config/www /srv/hass/DISABLED
```

dont think it was ever used





# Ideas/notes

## night mode in psyedo code:

```python
set triggers = [yellow_button, alarm_button, done_brushing]
if any(a.last_triggered > alarm_last_run):
    night_mode = true
else:
    night_mode = false
```

if yellow button/done brushing/orher alarm button
was pressed more recently than alarm start/stop,
theh set `night_mode`


## weather

possible condition values: https://developers.home-assistant.io/docs/core/entity/weather/#recommended-values-for-state-and-condition

## occupancy notes

VOC and CO2 are useful, when occupied:

 * VOC > 0.25-0.30 ppm
 * CO2 > 550-600 ppm

Their derivatives however are supririsngly less useful.


## Monitor

Powered on, charging laptop with USB-C: 40-80W
Standby (monitor off) charging a laptop: 7-25W
Powered on, without charging laptop (laptop connected with hdmi): ~23W (21-24W)
Standby, without charging laptop: <2W

Something like this could work?

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

