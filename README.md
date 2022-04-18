# KasaPoller
Polls data from TP-Link Kasa smart plug and sends to InfluxDB.
Tested with Raspberry PI and TP-Link HS110. The device must be in local mode, that is not connected to cloud account.
Make sure that the IP-address of the device remains static, for example by defining MAC-to-IP mapping
in router configuration.

Used library: https://github.com/python-kasa/python-kasa

## Build
Edit your InfluxDB configuration in my_config.py and then build image:
    docker build -t kasasender .

## Run

Run interactively:
    docker run --name kasasender --rm -e PLUG_IP=192.168.1.50 kasasender:latest

Run permanently:
    docker run --name kasasender -d --restart=always -e PLUG_IP=192.168.1.50 kasasender:latest
