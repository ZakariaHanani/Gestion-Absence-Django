# Generated by Django 5.0.1 on 2024-02-16 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfe', '0010_remove_attendance_dateattendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='Identifiant_Attendance',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
