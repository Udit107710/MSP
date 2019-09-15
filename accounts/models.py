from django.db import models
from django.contrib.auth.models import (

     PermissionsMixin,
)

from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField
from .validators import validate_possible_number
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Teacher(models.Model):
    USER_TYPE_CHOICES = [
        ("Student", 0),
        ("HOD", 1),
        ("AC", 3),
        ("Professor", 3)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teachers")
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    field_of_study = models.CharField(max_length=200)
    slots_occupied = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    phone = PhoneNumberField(null=True)
    department = models.CharField(max_length=200)
    type_of_user = models.IntegerField(choices=USER_TYPE_CHOICES, default=3)

    class Meta:
        permissions = [('manage_users', 'Can manage users'), ('manage_staff', "Can manage staff")]


class Student(models.Model):
    USER_TYPE_CHOICES = [
        ("Student", 0),
        ("HOD", 1),
        ("AC", 2),
        ("Professor", 3)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")
    enrollment_number = models.CharField(max_length=10)
    sap_id = models.CharField(max_length=10)
    program = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    cgpa = models.FloatField(blank=True)
    type_of_user = models.IntegerField(choices=USER_TYPE_CHOICES, default=3)

    class Meta:
        permissions = [('manage_users', 'Can manage users')]