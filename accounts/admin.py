from django.contrib import admin
from .models import User, Student, Teacher
from django.contrib.auth.forms import UserCreationForm


class CustomModelAdmin(admin.ModelAdmin):
    exclude = ['password']


admin.site.register(User, CustomModelAdmin)
admin.site.register(Student)
admin.site.register(Teacher)