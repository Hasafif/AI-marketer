import requests

url = 'http://localhost:8000/send_message'
file_path = 'e.txt'
url1 = 'http://localhost:8000/get'
# Create a dictionary to include any additional data if required
url2 = 'http://localhost:8000/content'
payload2 = {
    "name":"hu",
    "type":"web site",
    "link":"www.op.com",
    "description":"very uesful for educational purposes",
    "contact":"g6 team",
    "title":"promotion",
    "sender":"g6 company"
  
}

response2 = requests.post(url2, json=payload2)

if response2.status_code == 200:
    print("Message sent successfully")
    mess = response2.json()['choices'][0]['message']['content']
    print(mess)
else:
    print("Failed to send message:", response2.json()['message'])
payload1 = {}

# Open the file in binary mode and send it as part of the request
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url1,files=files,json=payload1)

# Check the response
if response.status_code == 200:
    print('File upload successful')
    message = response.json()
    print(message)
    payload = { 
   "api_key":"re_is9mRqzP_3NKtsczoW3GZs4x4ox6FmQtd",
   "from":"marketing <koora@chatg6.ai>",
   "subject":"hello world",
   "content":mess,
   "to": message
    }
    response1 = requests.post(url,json=payload)
    if response1.status_code == 200:
         print('File upload successful')
    else:
        print('File upload failed')
else:
    print('File upload failed')
