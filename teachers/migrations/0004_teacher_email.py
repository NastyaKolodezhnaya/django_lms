# Generated by Django 3.2.7 on 2021-10-09 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_auto_20211009_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=120, null=True),
        ),
    ]
