import requests
import json

url = "http://localhost:5051/v1/account/password"

payload = json.dumps({
  "login": "login10",
  "token": "16046253-a2aa-4e0a-ad52-61dd98bfd563",
  "oldPassword": "login_55",
  "newPassword": "login_555"
})
headers = {
  'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3tSjxTsDEJrXRPW+7nr8wvYMZWFwROnyXUUh9zf1jn5DDYIzEuNIAUR7PxWJnirYYs=',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
