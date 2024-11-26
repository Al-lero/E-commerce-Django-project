from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers

from user.models import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','username','first_name','last_name','email','password']


class UserLoginSerializer(TokenCreateSerializer):
    class Meta(TokenCreateSerializer):
        model = Customer
        fields = ['email', 'password']