from django.db import models
from accounts.models import Teacher


class ActivityCoordinator(models.Model):
    AC = models.OneToOneField(Teacher, on_delete=models.DO_NOTHING)
    Program = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.AC.user.first_name + " - " + self.Program