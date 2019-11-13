from django.contrib.auth.models import User
from .models import  Teacher
from student.models import Student

def check_student(username):
    user = Student.objects.filter(user__username=username)
    if user:
        return True
    else:
        return False


def check_teacher(username):
    user = Teacher.objects.filter(user__username=username)
    if user:
        if user.filter(type_of_user=2):
            return "Activity coordinator"
        elif user.filter(type_of_user=1):
            return "Head of Department"
        return "Professor"
    else:
        return False


def check_user(username):
    if check_student(username=username):
        return "Student"
    elif check_teacher(username=username) is not False:
        return check_teacher(username=username)
    else:
        return "SuperUser"
