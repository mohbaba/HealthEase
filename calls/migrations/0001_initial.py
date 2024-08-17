# Generated by Django 5.1 on 2024-08-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('duration', models.FloatField(default=0)),
            ],
        ),
    ]
