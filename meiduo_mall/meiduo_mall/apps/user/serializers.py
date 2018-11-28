import re

from rest_framework import serializers

from user.models import UserModel
from django_redis import get_redis_connection

class UserSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,allow_null=False,allow_blank=False)
    sms_code = serializers.CharField(write_only=True,allow_null=False,allow_blank=False)
    allow = serializers.BooleanField(write_only=True,default=None)
    class Meta:
        model = UserModel
        fields = ('id','username','password','password2','mobile','allow','sms_code')
        extra_kwargs = {
            'id':{'read_only':True},
            'username':{
                'min_length':5,
                'max_length':20,
                'error_exceptions':{
                    'min_length': "仅限于5-20个字符为用户名",
                    'max_length': "仅限于5-20个字符为用户名",
                }
            },
            'password':{
                'write_only':True,
                'min_length':8,
                'max_length':20,
                'error_exceptions':{
                    'min_length': "仅限于8-20个字符为密码",
                    'max_length': "仅限于8-20个字符为密码",
                }
            }
        }
    def validate_mobile(self, mobile):
        if re.match("1[3-9]\d{9}",mobile) is not True:
            raise serializers.ValidationError("手机号格式错误")
        return mobile
    def validate_allow(self, allow):
        if allow is False:
            raise serializers.ValidationError("请勾选同意框")
        return allow
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        sms_code = attrs['sms_code']

        if password != password2:
            raise serializers.ValidationError('两次密码不一致')

        redis = get_redis_connection('make_num')
        sm_code = redis.get('sms_%s'%sms_code)
        if sm_code is None:
            raise serializers.ValidationError('短信验证码已经失效')
        if sms_code != sm_code.decode():
            raise serializers.ValidationError('短信验证码错误')
    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        ress = super(UserSerializers, self).create(validated_data)
        ress.set_password(validated_data['password'])

        ress.save()
        return ress





