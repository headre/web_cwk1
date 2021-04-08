# Generated by Django 3.1.7 on 2021-04-08 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20210407_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authors',
            name='user',
        ),
        migrations.AddField(
            model_name='authors',
            name='password',
            field=models.CharField(default=None, max_length=16),
        ),
        migrations.AddField(
            model_name='authors',
            name='username',
            field=models.CharField(default=None, max_length=16, unique=True),
        ),
    ]