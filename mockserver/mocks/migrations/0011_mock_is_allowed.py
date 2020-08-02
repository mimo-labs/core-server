# Generated by Django 3.0.5 on 2020-08-02 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocks', '0010_project_slug_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mock',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mock',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
