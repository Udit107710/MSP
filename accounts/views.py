from rest_framework.views import APIView, View
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
import json
from .utils import check_user
import logging
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer
from django.template import loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from rest_framework import permissions

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
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        template = loader.get_template("accounts/index.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                qs = Teacher.objects.get(user__username=form.cleaned_data['username'])
            except:
                print(form.cleaned_data['username'])
                return HttpResponse(json.dumps({"status": "You're not a teacher"}), content_type="application/json")
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            if qs.type_of_user == 1:
                return redirect("hod-table", username=form.cleaned_data['username'])
            if qs.type_of_user == 2:
                return HttpResponse(json.dumps({"You are a AC"}), content_type="application/json")
            if qs.type_of_user == 3:
                return HttpResponse(json.dumps({"You are a professor!"}), content_type="application/json")
        return HttpResponse(json.dumps({"status": "Invalid form"}), content_type="application/json")


class HODTable(View):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        hod = Teacher.objects.get(user__username=username)
        department = hod.department
        teachers = Teacher.objects.filter(department=department).select_related("user")
        context = {'row': teachers}
        print(context)
        return render(request, "accounts/HoD_Table.html", context)
