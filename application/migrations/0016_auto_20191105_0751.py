# Generated by Django 2.2.4 on 2019-11-05 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20191104_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='member1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='member1', to='accounts.Student'),
        ),
        migrations.AlterField(
            model_name='project',
            name='member2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='member2', to='accounts.Student'),
        ),
        migrations.AlterField(
            model_name='project',
            name='member3',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='member3', to='accounts.Student'),
        ),
        migrations.AlterField(
            model_name='project',
            name='member4',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='member4', to='accounts.Student'),
        ),
    ]