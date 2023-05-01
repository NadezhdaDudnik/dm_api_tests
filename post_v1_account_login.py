import requests
import json

url = "http://localhost:5051/v1/account/login"

payload = json.dumps({
  "login": "login10",
  "password": "login_55",
  "rememberMe": True
})
headers = {
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
