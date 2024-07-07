import paho.mqtt.client as mqtt
from django.conf import settings
from .models import Notification
from . import views
from Baby import settings as baby_settings
from twilio.rest import Client
from django.utils import timezone
from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='624dc809-45e5-4a7e-bd92-f36425957490',
    secret_key='B07C522814BA8E777A18F322896A24E863A388686EDC039A1871B0EBD5819FAC',
)

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('BVP/baby')
        mqtt_client.subscribe('BVP/cry')
        mqtt_client.subscribe('BVP/urine')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    # initialize twilio client
    # account_sid = baby_settings.TWILIO_ACCOUNT_SID
    # auth_token = baby_settings.TWILIO_AUTH_TOKEN
    # client = Client(account_sid, auth_token)

    new_notification = Notification()
    new_notification.notification_text = msg.payload.decode()
    new_notification.received_at = timezone.now()
    topic = msg.topic
    if msg.topic == "BVP/baby":
        new_notification.priority_level = "High"
        msg_title = 'Baby not found'
        msg_body = 'Baby is not found with camera. Check the room.'
    elif msg.topic == "BVP/cry":
        new_notification.priority_level = "Medium"
        msg_title = "Baby crying"
        msg_body = "I'm crying mom and dad."
    elif msg.topic == "BVP/urine":
        new_notification.priority_level = "Low"
        msg_title = 'Baby urinated'
        msg_body = 'Baby has urinated. Change the cloth.'

    new_notification.save()

    # local fcm token for chrome browser
    # local_fcm_token = 'd58VgOrGD6sa89lf4hifdY:APA91bH0aEslcQPFRztLc8M64necl-DoQVfhv47Jx9KbXRWswjyUr_ZamNbjwvDYBNqausZ6LuYhGA5sLt8T6IhRxh3vAo3tmJib3beV2Sd0fZzkMRvxs3Z1FYCC2plmp7sG8se5wA2T'
    # views.send_notification([local_fcm_token], "Baby Vision Pro", msg.payload.decode(), image_url)

    response = beams_client.publish_to_interests(
        interests=['BVP-user-1'],
        publish_body={
            'web': {
                'notification': {
                    'title': msg_title,
                    'body': msg_body,
                    'deep_link': 'http://127.0.0.1:8000/dashboard/',
                },
            },
        },
    )

    print(f'Received message on topic: {topic} with payload: {msg.payload.decode()}')
    # send sms with twilio
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