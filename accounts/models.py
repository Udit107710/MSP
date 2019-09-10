from django.db import models
from django.contrib.auth.models import (

     PermissionsMixin,
)

from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from versatileimagefield.fields import VersatileImageField
from .validators import validate_possible_number
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    field_of_study = models.CharField(max_length=200)
    slots_occupied = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    phone = PhoneNumberField(null=True)
    department = models.CharField(max_length=200)
    is_ac = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)

    class Meta:
        permissions = [('manage_users', 'Can manage users'), ('manage_staff', "Can manage staff")]


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=10)
    sap_id = models.CharField(max_length=10)
    program = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    cgpa = models.FloatField(blank=True)

    class Meta:
        permissions = [('manage_users', 'Can manage users')]