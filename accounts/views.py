from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
import json
from .utils import check_user
import logging
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer
from django.template import loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('user__first_name')
    serializer_class = TeacherSerializer
    lookup_field = "user__username"


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "user__username"


class CheckUserType(APIView):
    def get(self, request, username):
        type_of_user = check_user(username)
        return HttpResponse(json.dumps({'type': type_of_user}), content_type="application/json", status=200)


class Index(APIView):
    def get(self, request):
        template = loader.get_template("accounts/index.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            qs = Teacher.objects.all().only('user__username')
            if {'user__username': form['username']} in list(qs):
                user = authenticate(request, username=form['username'], password=form['password'])
                login(request, user)
                return HttpResponse(json.dumps({"Status": "Logged in"}), content_type="application/json")
            return HttpResponse(json.dumps({"status": "You're not a teacher"}), content_type="application/json")
        return HttpResponse(json.dumps({"status": "Invalid form"}), content_type="application/json")
