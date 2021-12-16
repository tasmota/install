# These binaries are not official releases and are built from the latest development branch! 
## :warning: Flash responsibly! No support will be provided for issues with these binaries! :warning:

Stable release ✨ Tasmota ✨ firmware files found [here](https://github.com/tasmota/install/tree/main/firmware/release)

[![Build_special_firmware](https://github.com/Jason2866/Tasmota-build/actions/workflows/Build_special_firmware.yml/badge.svg)](https://github.com/Jason2866/Tasmota-build/actions/workflows/Build_special_firmware.yml)

## Build variants:
 - tasmota-battery - extremely cut down build for battery powered Tuya sensors
 - tasmota32c3 - Support for ESP32-C3 2M no OTA variant (tasmota32c3_2M)
 - tasmota32c3-bluetooth - BLE enabled
 - tasmota32s2 - Beta support for ESP32-S2 chip
 - tasmota32-ethernet - (ESP32 only) supports Sonoff SPM (only for devices with Ethernet hardware!)
 - tasmota32-zigbeebridge - ESP32 based [ZigbeeBridge](https://templates.blakadder.com/ewelink_ZB-GW03.html)
 - tasmota-zigbee - Zigbee for TI based chips (Esp8266 and ESP32)
 - tasmota-fullrules - Rules with all the features (expressions, If statements, MQTT subscription)
 - tasmota-allsensors - guess whats in ;-)
 - tasmota-mega - big binary, almost every sensor included, OTA possible only with minimal
 - tasmota-minicustom - even smaller minimal build (warning: it has **NO** Webserver, you have to use MQTT for control)
 - tasmota-gps - GPS driver enabled
 - tasmota-platinum - IT...IS...HUGE!!! nearly everzthing is enabled (only for devices with >=4Mb flash)
 - tasmota-titanium - as platinum with scripting and MFRC522 RFID reader enabled
 - tasmota-rangeextender - Experimental build where Tasmota acts as AP range extender
 - tasmota-scripting - all scripting features instead of rules + Smart Meter Interface enabled
 - tasmota-thermostat - Thermostat driver and temperature sensors (ESP32 has Bluetooth included)
 - tasmota32solo1-thermostat - ESP32 Single Core Thermostat driver and Bluetooth temperature sensors (used on Shelly Plus 1PM for example)
 - tasmota-teleinfo - Teleinfo French metering system, (MQTT, TLS included only for ESP32) 
 - tasmota-tls - MQTT TLS enabled
 - tasmota32-udisplay - ESP32 only, uses Universal Display Driver
