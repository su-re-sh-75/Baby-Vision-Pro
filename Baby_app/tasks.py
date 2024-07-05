from celery import shared_task
import pusher
from .models import Notification
from Baby import settings
import influxdb_client

pusher_client = pusher.Pusher(
    app_id=settings.APP_ID,
    key=settings.APP_KEY,
    secret=settings.APP_SECRET,
    cluster=settings.APP_CLUSTER,
)
bucket = "BVP"
org = "BVP"
token = "xEEu4SJEKXcSRXsTiQngcTPFG0TCzCr2LDWmxN887D9RFhRSRk7UqJsQMIaAObZpLKQXle23QtK_RY0k0sDNew=="
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

@shared_task
def send_notification_data():
    notification_data = Notification.objects.first()
    if notification_data:
        pusher_client.trigger('sensor-data-channel', 'sensor-data', {
            'message': notification_data.notification_text,
            'timestamp': notification_data.received_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

@shared_task
def query_influx():
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
    for record in result[0].records:
        results["humidity"].append((record.get_field(), record.get_value()))
    for record in result[1].records:
        results['temperature'].append((record.get_field(), record.get_value()))
    


