
import requests
import json

url = "http://localhost:5051/v1/account/email"

payload = json.dumps({
  "login": "login10",
  "password": "login_555",
  "email": "login100@mail.ru"
})
headers = {
  'X-Dm-Auth-Token': 'IQJh+zgzF5DjJbR86iLOoCJ6RiQBAGOf2xnz7Jgcy8ExyAVKa8GmvgWm5dtmzyFtJqRM1srNY3uEeVpwTryYujIU6qaU2sIYfhtd8UdpN9VZD7pXr/m+GRlWZd5Gqh3v2iGI5HpKph8=',
  'X-Dm-Bb-Render-Mode': '<string>',
  'Content-Type': 'application/json',
  'Accept': 'text/plain'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
