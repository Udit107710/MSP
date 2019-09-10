from django.urls import path
from .views import CheckType

urlpatterns = [
    path(r"check/<str:username>", CheckType.as_view(), name="check_user")
,]