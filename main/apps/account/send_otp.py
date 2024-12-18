import random
import requests
from django.conf import settings
from main.apps.account.models import ActivationSMSCode, User


def send_otp(phone_number):
    user_otp = ActivationSMSCode.objects.filter(
        phone_number=phone_number
        ).first()
    if user_otp and user_otp.otp:
        return False    
    random_code = random.randint(1000, 9999)
    if not user_otp:
        user_otp = ActivationSMSCode(phone_number=phone_number)
    user_otp.otp = random_code
    user_otp.save()   
    text = f"OTP code for Proclear: \n\n\n {random_code}" 
    url = "http://91.204.239.44/broker-api/send/"
    data = {
        "messages":
        [
            {
                "recipient": "998{}".format(phone_number),
                "message-id": "abc000000001",
                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": text
                    }
                }
            }
        ]
    }
    res = requests.post(
        url,
        headers={
            "Content-type": "application/json",
            "Authorization": "Basic {}".format(settings.SMS_AUTH_TOKEN)
        },
        json=data
    )
    if res.status_code == 200:
        return True
    return False


def resetting_otp(phone_number):
    phone_number = User.objects.get(phone_number=phone_number).phone_number
    resetting_code = random.randint(1000, 9999)
    print(resetting_code)
    user_activating_code = User.objects.get(phone_number=phone_number)
    user_activating_code.activating_code = resetting_code
    user_activating_code.save()   
    hash_code = settings.OTP_HASH_CODE
    text = f"OTP code for Proclear: \n\n\n {resetting_code} \n\n\n {hash_code}"
    url = "http://91.204.239.44/broker-api/send/"
    data = {
        "messages":
        [
            {
                "recipient": "998{}".format(phone_number),
                "message-id": "abc000000001",
                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": text
                    }
                }
            }
        ]
    }
    res = requests.post(
        url,
        headers={
            "Content-type": "application/json",
            "Authorization": "Basic {}".format(settings.SMS_AUTH_TOKEN)
        },
        json=data
    )
    if res.status_code == 200:
        return True
    return False