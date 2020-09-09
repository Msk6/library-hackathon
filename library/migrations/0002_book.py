# Generated by Django 3.1.1 on 2020-09-09 17:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=550)),
                ('author', models.CharField(max_length=250)),
                ('year_of_release', models.IntegerField()),
                ('ISBN', models.IntegerField(unique=True, validators=[django.core.validators.MinLengthValidator(13), django.core.validators.MaxLengthValidator(13)])),
                ('genre', models.TextField(max_length=650)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]