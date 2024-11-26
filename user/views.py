from django.shortcuts import render

from .models import Customer
from .serializer import UserSerializer
from rest_framework.mixins import CreateModelMixin


class UserRegisterViewSet(CreateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = UserSerializer

# Create your views here.
