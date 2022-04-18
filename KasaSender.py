#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, datetime, io, time, traceback
import asyncio
from kasa import SmartPlug
from kasa import SmartDeviceException
from influxdb import InfluxDBClient
from requests import ConnectionError

# my_config contains all the configuration parameters needed to send data to InfluxDB
import my_config as conf

# This application listens to RuuviTag broadcasts and sends data to InfluxDB database.

G_SEND_INTERVAL = 60

class KasaSender():
    plug = None

    def __init__(self, plug_ip):
        self.plug = SmartPlug(plug_ip)

    def start(self):
        asyncio.run(self.dataloop())

    async def dataloop(self):
        while True:
            try:
                await self.plug.update()
                json = self.create_influx_json()
#                print(json)
                self.send_data_to_influx(json)

            except SmartDeviceException:
                print(traceback.format_exc())

            except ConnectionError:
                print(traceback.format_exc())

            time.sleep(G_SEND_INTERVAL)

    def send_data_to_influx(self, jsondata):
        client = InfluxDBClient(conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER, conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE, timeout=5)
        client.write_points(jsondata)

    def create_influx_json(self):
        timestamp = datetime.datetime.utcnow()
        str_timestamp = timestamp.isoformat("T") + "Z"

        json_temp = [
            {
                "measurement": "power",
                "tags": {
                    "sensorId": self.plug.alias
                },
                "time": str_timestamp,
                "fields": {
                   "power": self.plug.emeter_realtime["power"],
                   "voltage": self.plug.emeter_realtime["voltage"],
                   "current": self.plug.emeter_realtime["current"],
                   "totalEnergy": self.plug.emeter_realtime["total"]
                }
            }
        ]

        return json_temp


###########################################
# Main function
###########################################

if __name__ == '__main__':

    print("KasaSender starting")
    sys.stdout.flush()

    plugIP = os.getenv("PLUG_IP")
    if not plugIP:
        raise ValueError("Define plug IP with environment variable PLUG_IP")

    sender = KasaSender(plugIP)

    try:
        sender.start()
    except KeyboardInterrupt:
        print("Shutting down after KeyboardInterrupt")
    except:
        print("Exception in KasaSender")
        print(traceback.format_exc())
        raise

