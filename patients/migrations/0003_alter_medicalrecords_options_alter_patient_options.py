# Generated by Django 5.0.7 on 2024-07-28 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicalrecords',
            options={'verbose_name': 'Medical Record', 'verbose_name_plural': 'Medical Records'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'Patient', 'verbose_name_plural': 'Patients'},
        ),
    ]
