from django.conf.urls import url

from verifications.views import ImageCodeVIew, Sms_codeView

urlpatterns = [
    url('^image_codes/(?P<image_code_id>.+)',ImageCodeVIew.as_view()),
    url('^sms_codes/(?P<mobile>1[3-9]\d{9})',Sms_codeView.as_view())
]