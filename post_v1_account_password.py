import requests
import json

url = "http://localhost:5051/v1/account/password"

payload = json.dumps({
  "login": "login10",
  "email": "login10@mail.ru"
})
headers = {
  'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3tSjxTsDEJrXRPW+7nr8wvYMZWFwROnyXUUh9zf1jn5DDYIzEuNIAUR7PxWJnirYYs=',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
