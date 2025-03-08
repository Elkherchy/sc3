# users/utils.py
import random
from django.conf import settings
from mailjet_rest import Client

def generate_password():
    return str(random.randint(100000, 999999))

def send_password_email(user_email, password_code):
    mailjet = Client(auth=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD), version='v3.1')
    
    data = {
      'Messages': [
        {
          "From": {
            "Email": "melotoukha@gmail.com",
            "Name": "SC3-2025"
          },
          "To": [
            {
              "Email": user_email,
              "Name": "User"
            }
          ],
          "Subject": "Your PASSWORD",
          "TextPart": f"Your password_code code is: {password_code}",
          "HTMLPart": f"<h3>Your password_code code is: <strong>{password_code}</strong></h3>",
        }
      ]
    }

    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print("password_code email sent successfully!")
    else:
        print(f"Failed to send password_code: {result.status_code}, {result.json()}")
