import requests
import json
import time

url = "http://192.168.29.212/data"


headers = {
  'Content-Type': 'application/json'
}

# response = requests.request("POST", url, headers=headers, json = payload)

# import requests

# url = 'https://api.example.com/api/dir/v1/accounts/9999999/orders'
headers = {'Accept' : 'text/html', 'Content-Type' : 'text/html'}

# payload = {"data": [123345567]}
# response = requests.post(url, data=payload, headers=headers)

# exit(0)

for i in range(100):
    payload = {"data": [i * 100000, i * 10000, i * 1000, i * 100, i * 10, i]}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    time.sleep(.02)
    print(i)