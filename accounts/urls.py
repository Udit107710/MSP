from django.urls import path
from .views import TeacherViewSet, StudentViewSet, UserViewSet, CheckUserType, Index

teacher_list = TeacherViewSet.as_view({
    'get': 'list'
})
student_list = StudentViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
student_detail = StudentViewSet.as_view({
    'get': 'retrieve'
})
teacher_detail = TeacherViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns = [
    path(r"teachers", teacher_list, name="teachers-list"),
    path(r"students", student_list, name="students-list"),
    path(r"user/<str:username>", user_detail, name="user-detail"),
    path(r"student/<str:user__username>", student_detail, name="student-detail"),
    path(r"teacher/<str:user__username>", teacher_detail, name="teacher-detail"),
    path(r"check/<str:username>", CheckUserType.as_view(), name="check-user-type"),

    #index page
    path('login/', Index.as_view(), name='index')
]