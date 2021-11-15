# Generated by Django 3.2.7 on 2021-11-15 12:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField(auto_now_add=True, null=True)),
                ('count_of_students', models.IntegerField(default=0)),
            ],
        ),
    ]
