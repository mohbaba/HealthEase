# Generated by Django 5.0.7 on 2024-07-28 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lab',
            options={'verbose_name': 'Lab', 'verbose_name_plural': 'Labs'},
        ),
        migrations.AddField(
            model_name='lab',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
