from django.shortcuts import render
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def index(request):
    return render(request, 'Baby_app/index.html')

def about(request):
    pass

def contact(request):
    pass

def signin(request):
    return render(request, 'Baby_app/signin.html')

def register(request):
    return render(request, 'Baby_app/signup.html')
    

def dashboard(request):
    
    bucket = "sensors"
    org = "BVP"
    token = "FOxPmFk6mKxzuqlWUC5AKwWZzXl1L8LIQ3wFhqL2l3DAMrSxPkAoB11vkfpijHGzhtDCZY4tsd3pvGxOjQFGMA=="
    url="http://localhost:8086"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    # Query script
    query_api = client.query_api()

    query = 'from(bucket:"sensors")\
    |> range(start: -30d)\
    |> filter(fn:(r) => r._measurement == "sensors")\
    |> filter(fn:(r) => r.location == "Prague")\
    |> filter(fn:(r) => r._field == "temperature")'

    result = query_api.query(org=org, query=query)
    context = {'temperature':[]}
    for table in result:
        for record in table.records:
            context['temperature'].append((record.get_time(), record.get_value()))

    return render(request, 'Baby_app/dashboard.html', context=context)