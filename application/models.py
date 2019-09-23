from django.db import models
from django.contrib.auth.models import User
from accounts.models import Student, Teacher


class Project(models.Model):
    def content_file_name(self, filename):
        return '/'.join(['files', self.title, filename])

    PROJECT_TYPE_CHOICES = [
        (0, "Minor-I"),
        (1, "Minor-II"),
        (2, "Major-III"),
        (3, "Major-IV"),
        (4, "Other")
    ]
    PROJECT_STATUS_CHOICES = [
        (0, "Proposed"),
        (1, "Accepted"),
        (2, "Rejected")
    ]

    project_type = models.IntegerField(choices=PROJECT_TYPE_CHOICES, default=4, null=True)
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=500, null=True)
    proposal = models.FileField(upload_to="proposals", null=True)
    associated_files = models.FileField(upload_to=content_file_name, blank=True, null=True)

    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, default=0, null=True)

    members = models.ManyToManyField(Student, null=True)
    mentor = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True)


