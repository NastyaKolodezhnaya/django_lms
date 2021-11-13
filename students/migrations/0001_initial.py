# Generated by Django 3.2.7 on 2021-11-13 10:22

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import students.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0004_alter_course_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(blank=True, max_length=120, null=True, validators=[students.validators.no_elon_validator, students.validators.prohibited_domains])),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator('\\d{10,14}')])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('birthdate', models.DateField(blank=True, default=datetime.date.today, null=True, validators=[students.validators.older_than_18])),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resume')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_course', to='courses.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
