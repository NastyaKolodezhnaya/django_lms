# Generated by Django 3.2.7 on 2021-11-13 10:22

from django.db import migrations, models
import students.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0004_alter_teacher_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=120, null=True, validators=[students.validators.no_elon_validator, students.validators.prohibited_domains]),
        ),
    ]
