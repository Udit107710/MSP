# Generated by Django 2.2.4 on 2019-09-02 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=200)),
                ('room_name', models.CharField(max_length=50)),
            ],
        ),
    ]
