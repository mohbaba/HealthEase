# Generated by Django 5.1 on 2024-08-17 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergies', models.CharField(choices=[('Lactose', 'Lactose'), ('Soy', 'Soy'), ('Seafood', 'Seafood'), ('Nuts', 'Nuts'), ('Eggs', 'Eggs'), ('Fish', 'Fish'), ('None', 'NONE'), ('Other', 'OTHER')], max_length=100)),
                ('current_medications', models.CharField(choices=[('21st Century fish oil', '21st Century fish oil'), ('Abidec', 'Abidec'), ('Accord Bendroflumethiazide', 'Accord Bendroflumethiazide'), ('ACCULOL', 'ACCULOL'), ('Actavis Doxycycline', 'Actavis Doxycycline'), ('Actinaza', 'Actinaza'), ('Aday kit tablets', 'Aday kit tablets'), ('Afrab vite', 'Afrab vite'), ('Africolo 1000 Capsules', 'Africolo 1000 Capsules')], max_length=100)),
                ('past_medications', models.CharField(choices=[('21st Century fish oil', '21st Century fish oil'), ('Abidec', 'Abidec'), ('Accord Bendroflumethiazide', 'Accord Bendroflumethiazide'), ('ACCULOL', 'ACCULOL'), ('Actavis Doxycycline', 'Actavis Doxycycline'), ('Actinaza', 'Actinaza'), ('Aday kit tablets', 'Aday kit tablets'), ('Afrab vite', 'Afrab vite'), ('Africolo 1000 Capsules', 'Africolo 1000 Capsules')], max_length=100)),
                ('chronic_disease', models.CharField(choices=[('Diabetes', 'Diabetes'), ('Hypertension', 'Hypertension'), ('PCOS', 'PCOS'), ('Hypothyroidism', 'Hypothyroidism'), ('COPD', 'COPD'), ('Asthma', 'Asthma'), ('None', 'NONE'), ('Other', 'OTHER')], max_length=100)),
                ('incident', models.CharField(choices=[('Burns', 'Burns'), ('Spinal Cord Injury', 'Spinal Cord Injury'), ('Spinal Fracture', 'Spinal Fracture'), ('Skull Fracture', 'Skull Fracture'), ('None', 'NONE'), ('Other', 'OTHER')], max_length=100)),
                ('surgeries', models.CharField(choices=[('Heart', 'HEART'), ('Liver', 'LIVER'), ('Kidney', 'KIDNEY'), ('Lungs', 'LUNGS'), ('Brain', 'BRAIN'), ('None', 'NONE'), ('Other', 'OTHER')], max_length=100)),
                ('smoking_habit', models.CharField(choices=[('I dont smoke', 'NOT_SMOKER'), ("I used to, but I've quit", 'NO_LONGER_SMOKER'), ('1 or more times per day', 'SMOKES')], max_length=100)),
                ('alcohol_habit', models.CharField(choices=[('Non-drinker', 'NON-DRINKER'), ('Rare', 'RARE'), ('Social', 'SOCIAL'), ('Regular', 'REGULAR'), ('Heavy', 'HEAVY')], max_length=100)),
                ('lifestyle', models.CharField(choices=[('Sedentary (low)', 'LOW'), ('Moderately active', 'MODERATELY'), ('Active (high)', 'HIGH'), ('Athletic (very high)', 'VERY HIGH')], max_length=100)),
                ('food_preferences', models.CharField(choices=[('Vegetarian', 'VEGETARIAN'), ('Non-Vegetarian', 'NON-VEGETARIAN'), ('Eggetarian', 'EGGETARIAN'), ('Vegan', 'VEGAN')], max_length=100)),
            ],
            options={
                'verbose_name': 'Medical Record',
                'verbose_name_plural': 'Medical Records',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Female', max_length=10)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+')], default='A+', max_length=5)),
                ('emergency_contact_name', models.CharField(default='null', max_length=40)),
                ('emergency_contact_phone', models.CharField(default='+23480000000', max_length=13)),
                ('doctors_notes', models.ManyToManyField(blank=True, related_name='notes', to='doctors.doctorsnote')),
                ('medical_records', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.medicalrecords')),
                ('newly_prescribed_medicine', models.ManyToManyField(blank=True, to='doctors.medicine')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
    ]
