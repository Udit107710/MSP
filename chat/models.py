from django.db import models

# Create your models here


class ChatMessage(models.Model):
    message = models.CharField(max_length=200)
    room_name = models.CharField(max_length=50)