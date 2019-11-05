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
        (1, "HOD"),
        (2, "AC"),
        (3, "Professor")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teachers", primary_key=True)
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
        (0, "Student")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="students", primary_key=True)
    enrollment_number = models.CharField(max_length=10)
    sap_id = models.CharField(max_length=10,unique=True)
    program = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    cgpa = models.FloatField(blank=True)
    type_of_user = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    lock = models.IntegerField(default=0)

    class Meta:
        permissions = [('manage_users', 'Can manage users')]