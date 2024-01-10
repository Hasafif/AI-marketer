import requests

url = 'http://localhost:8000/users'
payload = {
     "email": "hassan.n.afif@gmail.com",
    "id": "158",
    "email_provider":"Courier",
    "subscription":"Essential",
    "domain":"g6-company.com",
    "api_key":"pk_prod_012PXTFG6Q44VZPXTJ8ZCBP1WR4D"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Message sent successfully")
    #x = response.json()
    #print(x)
else:
    print("Failed to send message:", response.json()['message'])