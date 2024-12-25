import paho.mqtt.client as mqtt
from django.conf import settings
from .models import Notification
from . import views
from Baby import settings
from twilio.rest import Client
from django.utils import timezone
from pusher_push_notifications import PushNotifications
import pusher

# initializations of beams = Push notifications and Pusher client = channels
beams_client = PushNotifications(
    instance_id='',
    secret_key='',
)

pusher_client = pusher.Pusher(
    app_id=settings.APP_ID,
    key=settings.APP_KEY,
    secret=settings.APP_SECRET,
    cluster=settings.APP_CLUSTER,
)

def on_connect(mqtt_client, userdata, flags, rc):
    '''
    Operations to perform on connecting to mqtt_client
    '''
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('BVP/baby')
        mqtt_client.subscribe('BVP/cry')
        mqtt_client.subscribe('BVP/urine')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    '''
    Operations to perform on receiving message on mqtt 
    '''

    # initialize twilio client
    # account_sid = settings.TWILIO_ACCOUNT_SID
    # auth_token = settings.TWILIO_AUTH_TOKEN
    # client = Client(account_sid, auth_token)

    pusher_data = {} 
    new_notification = Notification()
    new_notification.notification_text = msg.payload.decode()
    new_notification.received_at = timezone.now()

    topic = msg.topic
    if msg.topic == "BVP/baby":
        new_notification.priority_level = "High"
        msg_title = 'Baby not found'
        msg_body = 'Baby is not found with camera. Check the room.'
        pusher_data['is_missing'] = True
    elif msg.topic == "BVP/cry":
        new_notification.priority_level = "Medium"
        msg_title = "Baby crying"
        msg_body = "I'm crying mom and dad."
        pusher_data['is_crying'] = True
    elif msg.topic == "BVP/urine":
        new_notification.priority_level = "Low"
        msg_title = 'Baby urinated'
        msg_body = 'Baby has urinated. Change the cloth.'
        pusher_data['is_urinated'] = True

    # save to DB, send data in channels, send push notification
    new_notification.save()
    pusher_client.trigger('notification-data-channel', 'notification-data', pusher_data)
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

    # send sms with twilio
    # message = client.messages.create(
    #      from_='+16504890117',
    #      body= msg.payload.decode(),
    #      to='+919342222369'
    #  )
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