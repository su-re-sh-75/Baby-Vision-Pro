from datetime import timedelta, datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import influxdb_client
import requests
from .mqtt import client as mqtt_client
from django.core.paginator import Paginator
from .models import Notification
from django.utils import timezone

bucket = "BVP"
org = "BVP"
token = "xEEu4SJEKXcSRXsTiQngcTPFG0TCzCr2LDWmxN887D9RFhRSRk7UqJsQMIaAObZpLKQXle23QtK_RY0k0sDNew=="
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def index(request):
    return render(request, 'Baby_app/index.html')

def get_initial_data(request):
    '''
    Returns a JSON with initial temp, humid data
    '''
    query_api = client.query_api()

    initial_data_query = 'from(bucket: "BVP")\
            |> range(start: -1d)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")'
    
    last_data_query = f'{initial_data_query}\
        |> last()'
    min_data_query = f'{initial_data_query}\
        |> min()'
    max_data_query = f'{initial_data_query}\
        |> max()'
    
    initial_data_result = query_api.query(org=org, query=initial_data_query)
    

    data = {
        'initial_humidity_data':[],
        'initial_temp_data':[],
    }
    if initial_data_result[0].records[0].get_field() == 'humidity':
        for record in initial_data_result[0].records:
            data["initial_humidity_data"].append({'x': record.get_time().astimezone().strftime('%Y-%m-%d %H:%M:%S'), 'y': round(record.get_value(), 2)})
    if initial_data_result[1].records[0].get_field() == 'temperature':
        for record in initial_data_result[1].records:
            data['initial_temp_data'].append({'x':record.get_time().astimezone().strftime('%Y-%m-%d %H:%M:%S'), 'y':round(record.get_value(), 2)})

    return JsonResponse(data)

def get_min_max_last_data(request):
    '''
    Returns a JSON with min, max, last values of temp and humid data
    '''
    query_api = client.query_api()
    base_query = 'from(bucket: "BVP")\
            |> range(start: -1d)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")'
    
    last_data_query = f'{base_query}\
        |> last()'
    min_data_query = f'{base_query}\
        |> min()'
    max_data_query = f'{base_query}\
        |> max()'
    
    last_data_result = query_api.query(org=org, query=last_data_query)
    min_data_result = query_api.query(org=org, query=min_data_query)
    max_data_result = query_api.query(org=org, query=max_data_query)

    data = {}
    data['last_humid'] = round(last_data_result[0].records[0].get_value(), 2)
    data['last_temp'] = round(last_data_result[1].records[0].get_value(), 2)
    data['min_humid'] = round(min_data_result[0].records[0].get_value(), 2)
    data['min_temp'] = round(min_data_result[1].records[0].get_value(), 2)
    data['max_humid'] = round(max_data_result[0].records[0].get_value(), 2)
    data['max_temp'] = round(max_data_result[1].records[0].get_value(), 2)

    return JsonResponse(data)

def get_notification_data(request):
    '''
    Returns a JSON with notification count data
    '''
    data = {
        'series_arr':[]
    }
    last_day = timezone.now() - timedelta(days=1)
    for i in ['Low', 'Medium', 'High']:
        data['series_arr'].append(Notification.objects.filter(priority_level=i, received_at__gte=last_day).count())
    print(data)
    return JsonResponse(data)
    

@login_required(login_url='/users/login/')
def dashboard(request):
    context = {}
    query = 'from(bucket: "BVP")\
            |> range(start: -1d)\
            |> filter(fn: (r) => r["_measurement"] == "sensor-data")\
            |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")\
            |> mean()'
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    context['avg_humid'] = round(result[0].records[0].get_value(), 2)
    context['avg_temp'] = round(result[1].records[0].get_value(), 2)

    last_day = timezone.now() - timedelta(days=1)
    context['cried_times'] = Notification.objects.filter(notification_text__contains="cry", received_at__gte=last_day).count()
    context['missed_times'] = Notification.objects.filter(notification_text__contains="not found", received_at__gte=last_day).count()
    context['urinated_times'] = Notification.objects.filter(notification_text__contains="urinated", received_at__gte=last_day).count()
    context['notifications'] = Notification.objects.order_by('-received_at')[:5]
    context['user'] = request.user
    return render(request, 'Baby_app/dashboard.html', context=context)

def livestream(request):
    url = f'http://192.168.41.81:5000/video_feed'
    try:
        response = requests.head(url, timeout=5)
        print(response)
        print(response.status_code)
        if response.status_code == 200:
            return render(request, 'Baby_app/livestream.html', {'livestream_url': url})
        else:
            messages.error(request, ('Live stream server is not active.'))
            return render(request, 'Baby_app/livestream.html')        
    except requests.RequestException:
        messages.error(request, ('Live stream server is not active.'))
        return render(request, 'Baby_app/livestream.html')
    
def view_notifications(request):
    received_days = request.GET.get('received', '30')
    high_filter = request.GET.get('high', "")
    medium_filter = request.GET.get('medium', "")
    low_filter = request.GET.get('low', "")

    notifications_list = Notification.objects.all()

    days_ago = datetime.now() - timedelta(days=int(received_days))
    notifications_list = notifications_list.filter(received_at__gte=days_ago)

    if high_filter != "":
        notifications_list = notifications_list.filter(priority_level='High')
    if medium_filter != "":
        notifications_list = notifications_list.filter(priority_level='Medium')
    if low_filter != "":
        notifications_list = notifications_list.filter(priority_level='Low')

    notifications_list = notifications_list.order_by('-received_at')

    paginator = Paginator(notifications_list, 10)  

    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)

    context = {
        'notifications': notifications,
        'received_days': received_days,
        'high_filter': high_filter,
        'medium_filter': medium_filter,
        'low_filter': low_filter,
    }

    return render(request, 'Baby_app/notification.html', context)

def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
