import paho.mqtt.client as mqtt
from django.conf import settings
from .models import Notification

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('BVP/baby')
        mqtt_client.subscribe('BVP/cry')
        mqtt_client.subscribe('BVP/urine')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    new_notification = Notification()
    new_notification.notification_text = msg.payload.decode()
    topic = msg.topic
    if msg.topic == "BVP/baby" or msg.topic == "BVP/cry":
        new_notification.priority_level = "High"
    elif msg.topic == "BVP/urine":
        new_notification.priority_level = "Medium"

    new_notification.save()

    print(f'Received message on topic: {topic} with payload: {msg.payload.decode()}')


client = mqtt.Client()
client.tls_set(ca_certs='./emqxsl-ca.crt')
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
client.loop_start()