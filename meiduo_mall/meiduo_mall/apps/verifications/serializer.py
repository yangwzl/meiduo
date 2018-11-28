from rest_framework import serializers
from django_redis import get_redis_connection
class checkIamgeSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4,min_length=4)
    image_code_id = serializers.UUIDField()
    def validate(self, attrs):
        text = attrs['text']
        image_code_id = attrs['image_code_id']
        redis_conn = get_redis_connection('verify_codes')
        image_code = redis_conn.get('img_%s' % image_code_id)
        try:
            redis_conn.delete('img_%s'% image_code_id)
        except Exception as e:
            pass
        if image_code is None:
            raise serializers.ValidationError('验证码已经失效')
        if image_code.decode().lower() != text.lower():
            raise serializers.ValidationError("验证码错误")
        return attrs











