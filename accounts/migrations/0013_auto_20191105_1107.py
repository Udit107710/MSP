# Generated by Django 2.2.4 on 2019-11-05 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_student_lock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sap_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]