# Generated by Django 2.2.4 on 2019-10-31 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20191030_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to='accounts.Student'),
        ),
    ]
