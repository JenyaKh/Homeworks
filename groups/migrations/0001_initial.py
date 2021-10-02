# Generated by Django 3.2.7 on 2021-10-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('faculty', models.CharField(max_length=80)),
                ('handler', models.EmailField(max_length=120, null=True)),
                ('start_year', models.CharField(default=2021, max_length=4, null=True)),
            ],
        ),
    ]
