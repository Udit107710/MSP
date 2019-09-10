from django.contrib import admin
from .models import User, Student, Teacher
from django.contrib.auth.forms import UserCreationForm

admin.site.register(Student)
admin.site.register(Teacher)