from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.utils import ExampleAuthentication
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
import json
import logging

logger = logging.getLogger(__name__)


class Login(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)

        logger.log(1, "Login data received for user")
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                login(request, user=user)
                return HttpResponse(json.dumps({"user": user.username, "error": ""}), status=200, content_type="application/json")
            else:
                return HttpResponse(json.dumps({"user": "", "error": "Invalid credentials"}), status=401, content_type="application/json")
        else:
            return HttpResponse(json.dumps({"user": "", "error": serializer.errors}), status=400, content_type="application/json")