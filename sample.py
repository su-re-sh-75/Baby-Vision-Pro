#!/bin/python3
import requests

url = 'http://192.168.11.90:8000/notify/'
params = {
    'msg': 'your_message',
    'topic': 'your_topic',
    'level': 'your_level'
}

response = requests.get(url, json=params)

print(response.text)
