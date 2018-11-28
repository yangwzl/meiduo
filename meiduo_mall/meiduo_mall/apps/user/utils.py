import re

from user.models import UserModel


def response_payload_handler(token,user=None,password=None):
    return {
        'token':token,
        'user_name':user.username,
        'user_id':user.id,
    }

def get_use_num(acctis):
    try:
        if re.match("1[3-9]\d{9}",acctis):
            user = UserModel.objects.filter(mobile=acctis).first()
        else:
            user = UserModel.objects.filter(username=acctis).first()
    except Exception as e:
        return None
    return user
from django.contrib.auth.backends import ModelBackend
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_use_num(username)
        if user is not None and user.check_password(password):
            return user
