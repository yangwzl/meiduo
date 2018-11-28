from django.shortcuts import render
from rest_framework.generics import CreateAPIView
# Create your views here.
from user.serializers import UserSerializers



class UserView(CreateAPIView):
    serializer_class =UserSerializers