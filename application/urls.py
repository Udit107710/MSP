from django.urls import path
from .views import ProposeProject

urlpatterns = [
    path(r"^propose/$", ProposeProject.as_view(), name="propose-project")
]