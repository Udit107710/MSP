from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from . import models


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
    })


@receiver(post_save, sender=models.ChatMessage)
def message_received(sender, instance, **kwargs):
    print('Model saved', instance.room_name, instance.message)
    channel_layer = get_channel_layer()
    room_name = instance.room_name
    message = instance.message

    async_to_sync(channel_layer.group_send)(
        'chat_' + room_name,
        {
            'type': 'chat_message',
            'message': message,
        }
    )
    print('sent')