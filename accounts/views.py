from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.utils import ExampleAuthentication
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
import json
from .utils import check_user
import logging

logger = logging.getLogger(__name__)


class CheckType(APIView):
    def get(self, request, username):
        type_of_user = check_user(username=username)
        return Response({"type": type_of_user}, content_type="application/json", status=200)
