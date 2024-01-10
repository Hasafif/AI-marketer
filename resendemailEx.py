import os
import resend

resend.api_key = "re_is9mRqzP_3NKtsczoW3GZs4x4ox6FmQtd"
mess = "go"
params = {
    "from": "ma <koora@chatg6.ai>",
    "to": ["hassan.n.afif@gmail.com"],
    "subject": "hello world",
    "html": mess,
}

email = resend.Emails.send(params)
print(email)