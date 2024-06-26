from datetime import timedelta, datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .mqtt import client as mqtt_client
from django.core.paginator import Paginator
from .models import Notification

fcm_token = ""

def index(request):
    return render(request, 'Baby_app/index.html')

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

@login_required(login_url='/users/login/')
def dashboard(request):
    '''
    bucket = "PiData"
    org = "BabyMonitoringApp"
    token = "X8fiTDmuE54FgUSG3v9mk6_5PUY9NclEM6z92p468k6KZ3gt4-v-xHPoUYPSPDSetZlR5K0uLT3L1-bal35h4A=="
    url="http://192.168.43.4:8000"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    # Query script
    query_api = client.query_api()

    query = 'from(bucket: "PiData")\
  |> range(start:-1d)\
  |> filter(fn: (r) => r["_measurement"] == "PI_TEST")\
  |> filter(fn: (r) => r["PI"] == "0")\
  |> filter(fn: (r) => r["_field"] == "Humidity_f" or r["_field"] == "Temperature_f" or r["_field"] == "Urinated")'

    result = query_api.query(org=org, query=query)
    context = {'temperature':[],
               'humidity':[],
               'urinated':[]
               }
    print(result)
    print(result[0].records)
    for table in result:
         for record in table.records:
             context['temperature'].append((record.get_field(), record.get_time(), record.get_value() ))
    '''
    context = {}
    context['user'] = request.user
    return render(request, 'Baby_app/dashboard.html', context=context)

@csrf_exempt
def store_token(request):
    if request.method == 'POST':
        global fcm_token
        data = json.loads(request.body)
        fcm_token = data.get('subscription')
        return JsonResponse({'message': 'Device saved successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def send_notification(registration_ids , message_title , message_desc, image_url):
    fcm_api = "AAAAeHlB-E8:APA91bGPxyh9eIwV8l86K3SJ01R_yUUTD_Y80WBbzTwC9JhORf9m2QsoyZqCEQLzGLH_tVAydW0Vs0kN9dvNBRC3RXDg_4oeOuYqQJAk2DKPJbAEBgzZk8N2V8K7sPbqtbKLfGcIUlT2"
    
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type":"application/json",
        "Authorization": f'key={fcm_api}'
    }

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : image_url,
            # "icon": icon_url,
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)

@csrf_exempt
def send(request):
    # fcm_token = registration
    resgistration  = ['fHTxbAlZK7sUCi8LQSsxua:APA91bFc-ZZZDQOa2DXvMwR_-aUsbYINDCrfpXJTaG1R5rrnMBwdn6JDRGdUzRIvx-Uhta4rxDjnNEc7qXcXWZN17sw7YZCyNZepP9ZC6EcI14ZFZkZTeIMXo1NsVjYIbjrJapRjOLRy']
    send_notification(resgistration , 'Baby Vision Pro' , 'Mama! I\'m crying', "./static/Baby_app/images/anya-crying-2.jpg")
    return HttpResponse("sent")

def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})

def async_dashboard(request, slug):
    '''
    Dashboard view for testing channels feature
    '''
    notifications = Notification.objects.all()[:5]
    return render(request, 'Baby_app/main.html', {'notifications':notifications})