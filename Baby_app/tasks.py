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
def send_sensor_data_stats():
    '''
    Sends mean, min, max values of Temperature, Humidity from InfluxDB
    '''
    base_query = 'from(bucket: "BVP")\
            |> range(start: -1d)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")'
    query_api = client.query_api()
    mean_query = f'{base_query}\
        |> mean()'
    last_data_query = f'{base_query}\
        |> last()'
    min_data_query = f'{base_query}\
        |> min()'
    max_data_query = f'{base_query}\
        |> max()'
    
    mean_result = query_api.query(org=org, query=mean_query)
    last_data_result = query_api.query(org=org, query=last_data_query)
    min_data_result = query_api.query(org=org, query=min_data_query)
    max_data_result = query_api.query(org=org, query=max_data_query)
    pusher_data = {}
    pusher_data['avg_humid'] = round(mean_result[0].records[0].get_value(), 2)
    pusher_data['avg_temp'] = round(mean_result[1].records[0].get_value(), 2)
    pusher_data['last_humid'] = round(last_data_result[0].records[0].get_value(), 2)
    pusher_data['last_temp'] = round(last_data_result[1].records[0].get_value(), 2)
    pusher_data['min_humid'] = round(min_data_result[0].records[0].get_value(), 2)
    pusher_data['min_temp'] = round(min_data_result[1].records[0].get_value(), 2)
    pusher_data['max_humid'] = round(max_data_result[0].records[0].get_value(), 2)
    pusher_data['max_temp'] = round(max_data_result[1].records[0].get_value(), 2)
    pusher_client.trigger('sensor-stats-data-channel', 'sensor-stats-data', pusher_data)

@shared_task
def send_sensor_data():
    query = 'from(bucket: "BVP")\
            |> range(start: -2s)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")'
    
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = {
        'humidity':[],
        'temperature':[]
    }
    for record in result[0].records:
        results["humidity"].append({'x': record.get_time().astimezone().strftime('%Y-%m-%d %H:%M:%S'), 'y': round(record.get_value(), 2)})
    for record in result[1].records:
        results['temperature'].append({'x': record.get_time().astimezone().strftime('%Y-%m-%d %H:%M:%S'), 'y': round(record.get_value(), 2)})
    pusher_client.trigger('sensor-data-channel', 'sensor-data', results)

    


