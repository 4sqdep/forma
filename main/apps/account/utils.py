import random
import string
import requests
from datetime import datetime, timedelta






def generate_random_otp():
    _int = "".join(random.choice(string.digits) for _ in range(4))
    return _int


def send_otp_to_telegram_group(otp, phone_number, chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    message = f"Your generated OTP is: {otp}. \nPhone number: {phone_number}"
    
    params = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        print("OTP sent to Telegram group successfully!")
    else:
        print("Failed to send OTP to Telegram:", response.text)



def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=length))
    return password


def send_password_to_telegram_group(password, phone_number, chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    message = f"Your generated password is: {password}. \nPhone number: {phone_number}"
    
    params = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        print("Password sent to Telegram group successfully!")
    else:
        print("Failed to send password to Telegram:", response.text)



def otp_expire_time():
    time = datetime.now() + timedelta(minutes=1)
    return time.strftime('%H:%M:%S')
