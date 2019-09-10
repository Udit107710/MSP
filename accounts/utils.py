from django.contrib.auth.models import User
from .models import Student, Teacher


def check_student(username):
    user = Student.objects.filter(user__username=username, is_student=True)
    if user:
        return True
    else:
        return False


def check_teacher(username):
    user = Teacher.objects.filter(user__username=username, is_professor=True)
    if user:
        if user.is_ac:
            return "Activity coordinator"
        elif user.is_hod:
            return "Head of Department"
        return "Professor"
    else:
        return False


def check_user(username):
    if check_student(username=username):
        return "Student"
    else:
        if check_teacher(username=username) is not False:
            return check_teacher(username=username)
        else:
            return "SuperUser"