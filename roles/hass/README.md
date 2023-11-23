# hass

[![Home Assistant logo](home-assistant.svg)](https://design.home-assistant.io/#brand/logo)

Documentation: [`www.sudo.is/docs/hass`](https://www.sudo.is/docs/hass)

Roles:

 * [`roles/hass-core`](../hass-core/): Home Assistant
 * [`roles/hass-zwave`](../hass-zwave/): Z-Wave JS for Z-Wave devices.
 * [`roles/hass-esphome`](../hass-esphome/): ESPhome configs and packages,
 * [`roles/hass-appdaemon`](../hass-appdaemon/): Automations written in pure python.
 * [`roles/hass-nginx`](../hass-nginx/): Configs for Nginx reverse proxy config, including for zwave-js.
 * [`roles/hass-zigbee`](../hass-zigbee/): Unfortunate misfit requiring MQTT, but the IKEA devices are great. Considering
   switching to [the deCONZ integration](https://www.home-assistant.io/integrations/deconz/) instead, as that uses
   websockets.
 * [`roles/hass-ser2net`](../hass-ser2net/): Exposes Z-Wave and ZigBee USB sticks' serial interfaces over TCP.
 * [`roles/hass-utils`](../hass-utils/): Various scripts to deal with weidnesses.
