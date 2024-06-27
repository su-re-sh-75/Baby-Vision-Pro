# python 3.8

import random
import time

from paho.mqtt import client as mqtt_client


host = 'p1d3f813.ala.asia-southeast1.emqxsl.com'
port = 8883
topic = ["BVP/baby", "BVP/urine", "BVP/cry"]
# topic = ["BVP/baby"]
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'suresh'
password = 'suresh'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)
    return client


def publish(client):
    msg_count = 0
    while msg_count != 2:
        for i in topic:
            time.sleep(2)
            if i == "BVP/baby":
                msg = "Baby not found!"
                result = client.publish(i, msg)
                # result: [0, 1]
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{i}`")
                else:
                    print(f"Failed to send message to topic {topic}")
            elif i == "BVP/cry":
                msg = "Mama, I'm crying!"
                result = client.publish(i, msg)
                # result: [0, 1]
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{i}`")
                else:
                    print(f"Failed to send message to topic {topic}")
            elif i == "BVP/urine":
                msg = "Baby urinated! change the diaper."
                result = client.publish(i, msg)
                # result: [0, 1]
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{i}`")
                else:
                    print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()