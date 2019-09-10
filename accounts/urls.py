from django.urls import path, re_path
from .views import CheckType

urlpatterns = [
    re_path(r"check$", CheckType.as_view(), name="check_user")
,]