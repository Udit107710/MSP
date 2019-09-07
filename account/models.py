from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from django.db.models import Q, Value
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from versatileimagefield.fields import VersatileImageField
from .validators import validate_possible_number
from django.core.validators import MaxValueValidator, MinValueValidator


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_hod=False, is_ac=False, is_professor=False,is_staff=False, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_ac=is_ac, is_hod=is_hod, is_professor=is_professor, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_ac=True, is_superuser=True, is_hod=True, is_professor=True, is_staff=True, **extra_fields
        )

    def students(self):
        return self.get_queryset().filter(is_ac=False, is_professor=False, is_hod=False, is_superuser=False)


def get_token():
    return str(uuid.uuid4())


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    token = models.UUIDField(default=get_token, editable=False, unique=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    phone = PhoneNumberField(null=True)
    department = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_ac = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        permissions = [('manage_users', 'Can manage users'), ('manage_staff', "Can manage staff")]


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field_of_study = models.CharField(max_length=200)
    slots_occupied = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=10)
    sap_id = models.CharField(max_length=10)
    program = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    cgpa = models.FloatField(blank=True)