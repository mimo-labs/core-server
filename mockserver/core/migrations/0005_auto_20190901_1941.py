# Generated by Django 2.1.11 on 2019-09-01 19:41

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190901_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mock',
            name='content',
            field=models.TextField(default='{}', validators=[core.validators.validate_json]),
        ),
        migrations.AlterField(
            model_name='mock',
            name='params',
            field=models.TextField(default='{}', validators=[core.validators.validate_json]),
        ),
        migrations.AlterField(
            model_name='mock',
            name='path',
            field=models.CharField(default='/', max_length=955, validators=[core.validators.validate_path]),
        ),
    ]