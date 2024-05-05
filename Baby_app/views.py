from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def index(request):
    return render(request, 'Baby_app/index.html')

def about(request):
    pass

def contact(request):
    pass

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
    context ={}
    return render(request, 'Baby_app/dashboard.html', context=context)