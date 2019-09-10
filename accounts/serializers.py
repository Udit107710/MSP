from . import models
from django.contrib.auth.models import User
from rest_framework import serializers


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']