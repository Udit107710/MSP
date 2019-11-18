from rest_framework.views import APIView, View
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
import json
from .utils import check_user
import logging
from .models import Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer
from django.template import loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from application.models import Project
from student.models import Student

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
                return HttpResponse(json.dumps({"status": "You're not a teacher"}), content_type="application/json", status=status.HTTP_404_NOT_FOUND)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            else:
                return HttpResponse(json.dumps({"status":"User not found!"}), content_type="application/json")
            if qs.type_of_user == 1:
                return redirect("hod-table")
            if qs.type_of_user == 2:
                return redirect("ac-table")
            if qs.type_of_user == 3:
                return HttpResponse(json.dumps({"status":"You are a professor!"}), content_type="application/json")
        return HttpResponse(json.dumps({"status": "Invalid form"}), content_type="application/json")


class HODTable(View):
    # permission_classes = [permissions.AllowAny]

    def get(self, request):
        username = request.user.username
        hod = Teacher.objects.get(user__username=username, type_of_user=1)
        department = hod.department
        data = Project.objects.filter(mentor__department=department)
        context = {'row': data}
        return render(request, "accounts/HoD_Table.html", context)


class ACTable(View):
    # permission_classes = [permissions.AllowAny]

    def get(self, request):
        username = request.user.username
        ac = Teacher.objects.get(user__username=username, type_of_user=2)

        qs1 = Project.objects.filter(member1__program__AC=ac)
        qs2 = Project.objects.filter(member2__program__AC=ac)
        qs3 = Project.objects.filter(member3__program__AC=ac)
        qs4 = Project.objects.filter(member4__program__AC=ac)
        qs = qs1 | qs2 | qs3 | qs4
        context = {'row': qs}
        return render(request, "accounts/AC_Table.html", context)
