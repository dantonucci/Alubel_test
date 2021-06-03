

# %% 
# ==================  GET TOKEN ================== 
import requests
import json

url = "http://127.0.1:5001/auth"

payload = json.dumps({
  "username": "mario",
  "password": "miao"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

Result = response.json()
valid_token = Result['access_token']


# ==================== MAKE A REQUEST ==============

url = "http://127.0.1:5001/Postjson/NewAirDB"


# Right File
file = "/Users/dantonucci/Alubel/Esempi_json/json with session and project.json"
# Wrong File
# file = "/Users/dantonucci/Alubel/Esempi_json/json_errato_2.json"
# file = "/Users/dantonucci/Alubel/Esempi_json/json_errato.json"

with open(file) as json_file:
    data = json.load(json_file)

payload = json.dumps(data)

headers = {
  'Authorization': f'JWT {valid_token}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
