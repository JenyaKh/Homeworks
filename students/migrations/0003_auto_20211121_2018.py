# Generated by Django 3.2.7 on 2021-11-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('students', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='course',
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.ManyToManyField(to='courses.Course'),
        ),
    ]