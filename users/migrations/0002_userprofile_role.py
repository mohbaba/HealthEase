# Generated by Django 5.1 on 2024-08-19 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('PATIENT', 'PATIENT'), ('DOCTOR', 'DOCTOR'), ('PHARMACIST', 'PHARMACIST'), ('LABORATORY', 'LABORATORY')], default='PATIENT', max_length=15),
        ),
    ]