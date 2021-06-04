# RestApi EEB Monitoring

The RestApi is used to send data from monitoring system to the influxdb.

## Registration 
Ask to the Administrator the credentials to use the restAPI. 

## Endpoints
### Main Endpoints

Hereunder the main endpoints of the API: 
url = https://eeb-testapi.herokuapp.com

1) USER LOGIN 
```
    {{url}}/login 
```
provide credentials as json/content:

    {
        email: ...
        password: ...
    }

output is the user-token. 

2) POST DATA    
```
    {{url}}/PostJson/<Name of the project>
```
the list of the "Name of the project" will be provided by the Administator

To POST the data is required the user token in the header. 
Example in Test.py

```
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
```
