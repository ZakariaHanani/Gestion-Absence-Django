# Generated by Django 5.0.1 on 2024-03-14 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfe', '0015_remove_student_identifiant_annee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seance',
            name='Identifiant_Annee',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='Identifiant_Filiere',
        ),
    ]