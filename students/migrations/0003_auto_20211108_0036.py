# Generated by Django 3.2.7 on 2021-11-07 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0002_auto_20211107_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('mentor', 'Mentor')], max_length=7),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]