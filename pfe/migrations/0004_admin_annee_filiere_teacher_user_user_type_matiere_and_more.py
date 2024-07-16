# Generated by Django 5.0.1 on 2024-01-26 14:22

import django.db.models.deletion
import pfe.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfe', '0003_remove_user_date_joined_remove_user_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('pfe.user',),
            managers=[
                ('objects', pfe.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Annee',
            fields=[
                ('Identifiant_Annee', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('Identifiant_Filiere', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('pfe.user',),
            managers=[
                ('objects', pfe.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('admin', 'Admin'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('Identifiant_Matiere', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50)),
                ('Identifiant_Filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.filiere')),
            ],
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('Identifiant_Seance', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50)),
                ('DateSeance', models.DateField()),
                ('HeureDebut', models.TimeField()),
                ('HeureFin', models.TimeField()),
                ('Identifiant_Annee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.annee')),
                ('Identifiant_Filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.filiere')),
                ('Identifiant_Matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.matiere')),
                ('Identifiant_Professeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Identifiant_Annee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.annee')),
                ('Identifiant_Filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.filiere')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('pfe.user',),
            managers=[
                ('objects', pfe.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(default='Absent', max_length=20)),
                ('DateAttendance', models.DateField(auto_now=True)),
                ('Identifiant_Matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.matiere')),
                ('Identifiant_Seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.seance')),
                ('Identifiant_Etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfe.student')),
            ],
        ),
    ]