# Generated by Django 2.2.15 on 2020-09-19 01:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slaves_app', '0002_datahistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='datahistory',
            name='jobid',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='datahistory',
            name='slaveid',
            field=models.CharField(default=1, max_length=5),
        ),
        migrations.AddField(
            model_name='slave',
            name='job_id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='slave',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='slave',
            name='slave_address',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(247), django.core.validators.MinValueValidator(1)]),
        ),
    ]
