# Generated by Django 3.0.3 on 2020-02-09 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_organization_profile'),
        ('tenants', '0006_organization_invite_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('avatar', models.ImageField(default='default.png', upload_to='')),
                ('website', models.URLField(null=True)),
                ('twitter', models.CharField(max_length=512, null=True)),
                ('facebook', models.CharField(max_length=512, null=True)),
                ('linkedin', models.CharField(max_length=512, null=True)),
                ('instagram', models.CharField(max_length=512, null=True)),
                ('technologies', models.ManyToManyField(blank=True, to='base.Technology')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenants.OrganizationProfile'),
        ),
    ]
