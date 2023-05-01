import requests

url = "http://localhost:5051/v1/account/c4efef0c-6646-47c4-9ae9-3d74ca439dd6"

payload = {}
headers = {
  'X-Dm-Auth-Token': '<string>',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Accept': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
