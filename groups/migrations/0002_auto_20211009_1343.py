# Generated by Django 3.2.7 on 2021-10-09 10:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='st_number',
            new_name='student_num',
        ),
        migrations.RemoveField(
            model_name='group',
            name='group_name',
        ),
        migrations.AlterField(
            model_name='group',
            name='start_date',
            field=models.DateTimeField(default=datetime.date(2021, 10, 9), null=True),
        ),
    ]
