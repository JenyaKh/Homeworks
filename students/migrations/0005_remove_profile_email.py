# Generated by Django 3.2.7 on 2021-11-09 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]