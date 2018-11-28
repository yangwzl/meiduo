from django.conf.urls import url

from user.views import UserView

urlpatterns = [
    url('^users/',UserView.as_view())
]