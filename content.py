import requests
url = 'http://localhost:8000/content'
payload = {
    "name":"g6",
    "type":"desktop app",
    "link":"www.op.com",
    "description":"very uesful for educational purposes",
    "contact":"hasan afif",
    "title":"promotion",
    "sender":"g6 company"
  
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Message sent successfully")
    message = response.json()['choices'][0]['message']['content']
    print(message)
else:
    print("Failed to send message:", response.json()['message'])