# Generated by Django 2.1.11 on 2019-10-14 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190901_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='header',
            name='header_type',
        ),
        migrations.RemoveField(
            model_name='header',
            name='mock',
        ),
        migrations.RemoveField(
            model_name='mock',
            name='verb',
        ),
        migrations.DeleteModel(
            name='Header',
        ),
        migrations.DeleteModel(
            name='HeaderType',
        ),
        migrations.DeleteModel(
            name='HttpVerb',
        ),
        migrations.DeleteModel(
            name='Mock',
        ),
    ]