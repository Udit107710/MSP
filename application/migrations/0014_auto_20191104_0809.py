# Generated by Django 2.2.4 on 2019-11-04 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20191104_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='member1',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='member1', to='accounts.Student'),
        ),
    ]