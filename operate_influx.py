#!/bin/python3

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

bucket = "BVP"
org = "BVP"
token = "xEEu4SJEKXcSRXsTiQngcTPFG0TCzCr2LDWmxN887D9RFhRSRk7UqJsQMIaAObZpLKQXle23QtK_RY0k0sDNew=="
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def influx_write():
    # Write script
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for i in range(1, 51):
        temperature = random.uniform(20, 30)  # Generate random temperature between 20 and 30
        humidity = random.uniform(40, 60)  # Generate random humidity between 40 and 60

        point = influxdb_client.Point("sensor-data").tag("device", "sensor").field("temperature", temperature).field("humidity", humidity)
        write_api.write(bucket=bucket, org=org, record=point)
        print(i, "Written", temperature, humidity)
        time.sleep(10)  

def influx_read():
    query = 'from(bucket: "BVP")\
            |> range(start: -1d)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")'
    
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = {
        'humidity':[],
        'temperature':[]
    }
    print(result)
    for record in result[0].records:
        results["humidity"].append(round(record.get_value(), 2))
    for record in result[1].records:
        results['temperature'].append(round(record.get_value(), 2))

    print(results["humidity"])
    print()
    print(results["temperature"])
    print(len(results["temperature"]))

if __name__ == "__main__":
    influx_write()