import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from influxdb_client.client.write_api import SYNCHRONOUS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .mqtt import client as mqtt_client
from django.core.paginator import Paginator
from .models import Notification

fcm_token = ""

def index(request):
    return render(request, 'Baby_app/index.html')

def view_notifications(request):
    notifications_list = Notification.objects.all().order_by('-received_at')  # fetch all notifications, newest first
    paginator = Paginator(notifications_list, 10)  # Show 10 notifications per page

    page_number = request.GET.get('page')
    notifications = paginator.get_page(page_number)

    return render(request, 'Baby_app/notification.html', {'notifications': notifications})

@login_required(login_url='/users/login/')
def dashboard(request, title=None, msg=None, img_url=None):
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
    if title or msg or img_url:
        context['notification'] = {'title':title, 
                                'msg':msg,
                                'img_url':img_url} 
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