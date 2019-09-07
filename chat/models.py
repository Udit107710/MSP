from django.db import models

# Create your models here


class ChatMessage(models.Model):
    sender = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    room_name = models.CharField(max_length=50)