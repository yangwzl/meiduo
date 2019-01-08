from django.conf.urls import url

from meiduo_mall.meiduo_mall.apps.user.views import UserView

urlpatterns = [
    url('^users/',UserView.as_view())
]