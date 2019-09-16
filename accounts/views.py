from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, HttpResponse
import json
from .utils import check_user
import logging
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = "user__username"


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "user__username"
