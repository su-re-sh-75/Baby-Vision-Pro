import paho.mqtt.client as mqtt
from django.conf import settings
from .models import Notification
from . import views
from Baby import settings as baby_settings
from twilio.rest import Client
from django.utils import timezone


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('BVP/baby')
        mqtt_client.subscribe('BVP/cry')
        mqtt_client.subscribe('BVP/urine')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    # account_sid = baby_settings.TWILIO_ACCOUNT_SID
    # auth_token = baby_settings.TWILIO_AUTH_TOKEN
    # client = Client(account_sid, auth_token)

    new_notification = Notification()
    new_notification.notification_text = msg.payload.decode()
    new_notification.received_at = timezone.now()
    topic = msg.topic
    icon_url = "./static/Baby_app/images/sleeping-baby.png"
    if msg.topic == "BVP/baby":
        new_notification.priority_level = "High"
        image_url = "./static/Baby_app/images/anya-hiding-crop.jpg"
    elif msg.topic == "BVP/cry":
        new_notification.priority_level = "High"
        image_url = "./static/Baby_app/images/anya-crying-2.jpg"
    elif msg.topic == "BVP/urine":
        new_notification.priority_level = "Medium"
        image_url = "./static/Baby_app/images/baby-urinated.jpg"

    new_notification.save()

    local_fcm_token = 'd58VgOrGD6sa89lf4hifdY:APA91bH0aEslcQPFRztLc8M64necl-DoQVfhv47Jx9KbXRWswjyUr_ZamNbjwvDYBNqausZ6LuYhGA5sLt8T6IhRxh3vAo3tmJib3beV2Sd0fZzkMRvxs3Z1FYCC2plmp7sG8se5wA2T'
    # views.send_notification([views.fcm_token], "Baby Vision Pro", msg.payload.decode(), image_url)
    views.send_notification([local_fcm_token], "Baby Vision Pro", msg.payload.decode(), image_url)
    print(f'Received message on topic: {topic} with payload: {msg.payload.decode()}')
    # message = client.messages.create(
    #     from_='+16504890117',
    #     body= msg.payload.decode(),
    #     to='+919342222369'
    # )
    # print(message.sid)

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