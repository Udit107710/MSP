from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from core.models import ActivityCoordinator


class Student(models.Model):
    USER_TYPE_CHOICES = [
        (0, "Student")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="students", primary_key=True)
    enrollment_number = models.CharField(max_length=10)
    sap_id = models.CharField(max_length=10, unique=True)
    program = models.ForeignKey(ActivityCoordinator, on_delete=models.DO_NOTHING, unique=False)
    semester = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    CGPA = models.FloatField(blank=True, validators=[MaxValueValidator(10), MinValueValidator(0)])
    lock = models.IntegerField(default=0)
    type_of_user = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)

    class Meta:
        permissions = [('manage_users', 'Can manage users')]

    def __str__(self):
        return self.user.email
