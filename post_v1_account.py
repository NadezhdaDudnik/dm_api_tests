import requests
import json

url = "http://localhost:5051/v1/account"

payload = json.dumps({
  "login": "login10",
  "email": "login10@mail.ru",
  "password": "login_55"
})
headers = {
  'X-Dm-Auth-Token': '<string>',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
