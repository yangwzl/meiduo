import random

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from meiduo_mall.libs.captcha.captcha import captcha

# Create your views here.
from meiduo_mall.utils.setting_time import IMAGE_CODE_TIME, SMS_CODE_TIME
from verifications.serializers import SmsCodeSerializer


class ImageCodeVIew(APIView):
    def get(self,request,image_code_id):
        text,image = captcha.generate_captcha()
        print("SSSSSSSSSS",text,image_code_id)
        redis_conn = get_redis_connection('make_num')

        redis_conn.setex('img_%s'%image_code_id,IMAGE_CODE_TIME,text)

        return HttpResponse(image,content_type='image/jpg')

from rest_framework.generics import GenericAPIView

class Sms_codeView(GenericAPIView):
    serializer_class = SmsCodeSerializer
    def get(self,request,mobile):
        ress = self.get_serializer(data=request.query_params)
        ress.is_valid(raise_exception=True)

        sms_code = "%06d"%random.randint(0,999999)
        print("ASSSSSSSSSSSSSSSS",sms_code)
        redis_conn = get_redis_connection('make_num')
        redis_conn.setex('sms_%s'%mobile,SMS_CODE_TIME,sms_code)

        ##/*/*/*/*/*/*/*

        return Response({'massage':"OK"},status=200)


