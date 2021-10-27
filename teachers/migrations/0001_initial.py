# Generated by Django 3.2.7 on 2021-10-26 12:22

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(max_length=120, null=True, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('course', models.ManyToManyField(to='courses.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
