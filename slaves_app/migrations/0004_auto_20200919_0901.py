# Generated by Django 2.2.15 on 2020-09-19 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slaves_app', '0003_auto_20200919_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slave',
            name='job_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
