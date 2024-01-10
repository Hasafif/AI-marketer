from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import requests
import resend
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hyf3'
app.config['MYSQL_DB'] = 'Marketers'
mysql = MySQL(app)
@app.route('/get', methods=['POST'])
def get():
    # Handle the file upload here
    file = request.files['file']
    file_content = file.read().decode('utf-8')
    # Split the file content by commas to extract the emails
    email_list = file_content.split(',')
    # Remove leading/trailing whitespace from each email
    emails = [email.strip() for email in email_list]
    return emails
@app.route('/send_message', methods=['POST'])
def send_message():
    api_key = request.json['api_key']
    From = request.json['from']
    subject = request.json['subject']
    content = request.json['content']
    to = request.json['to']
    resend.api_key = api_key
    params = {
     "from": From,
     "to": to,
     "subject": subject,
     "html": content,
     }

    email = resend.Emails.send(params)
    return email
@app.route('/users', methods=['POST'])
def add_data():
    cur = mysql.connection.cursor()
    email = request.json['email']
    id = request.json['id']
    email_provider = request.json['email_provider']
    api_key = request.json['api_key']
    domain = request.json['domain']
    subscription = request.json['subscription']
    cur.execute('''INSERT INTO users (email, id,email_provider,api_key,domain,subscription)  VALUES (%s, %s, %s, %s, %s, %s)''', (email, id,email_provider,api_key,domain,subscription))
    cur = mysql.connection.cursor()
    table_name = f"user_{id}_products"
    # Create a table named 'products' for the current user
    create_table_query = f"""
    CREATE TABLE {table_name} (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(255),
        price DECIMAL(10, 2),
        Marketing_strategy ENUM('Email','Social Media','Both')
    );
    """
    cur.execute(create_table_query)
    cur.close()
    return jsonify({'message': 'Data added successfully'})
@app.route('/data', methods=['GET'])
def get_data_by_id():
    cur = mysql.connection.cursor()
    id = request.json['id']
    cur.execute('''SELECT * FROM user WHERE id = %s''', (id,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
@app.route('/products', methods=['GET'])
def add_products():
       cur = mysql.connection.cursor()
       id = request.json['user_id']
       product_id = request.json['product_id']
       product_name = request.json['product_name']
       price = request.json['price']
       Marketing_strategy = request.json['Marketing_strategy']
       cur.execute('''INSERT INTO user_158_products (product_id, product_name,price,Marketing_strategy)  VALUES (%s, %s, %s, %s)''',(product_id, product_name,price,Marketing_strategy))
       mysql.connection.commit()
       cur.close()
       return jsonify({'message': 'Data added successfully'})
@app.route('/content', methods=['POST'])
def ask():
    name  = request.json['name']
    type = request.json['type']
    link = request.json['link']
    description = request.json['description']
    contact = request.json['contact']
    title = request.json['title']
    sender = request.json['sender']
    #if (strategy == "Email Marketing"):
    # Define the API endpoint URL
    api_url = 'https://api.openai.com/v1/chat/completions'
    # Set your OpenAI API key
    api_key = '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'
   
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
    }

    # Define the payload for the API request
    payload = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content':'Provide a professional email to promote ' + name + ' as a new ' + type + '. Fill out the email form as follows: \n\nContact Information: ' + contact + '\n\n[Your Name]: ' + sender + '\n[Your Title]: ' + title + '\n\nDear [Recipient Name],\n\nTo whom it may concern,\n\nInclude the following product description:\n\n' + description + '\n\nProduct Link:\n' + link + '\n\nPlease refrain from adding a subject line to the email.\n\nMoreover, ensure that the email adheres to SEO rules and is written in a powerful manner.\n\nWe kindly request you to use a formal tone throughout the email by referring to our company as (the ... company, our company) or our association as (the ... association, our association) instead of using personal pronouns (I, we, they).\n\nThank you for your attention.\n\nSincerely,'}
    ]
    }
    # Make the API request
    response = requests.post(api_url, headers=headers, json=payload)

    # Parse the response
    data = response.json()
    message = data['choices'][0]['message']['content']
    return data
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
