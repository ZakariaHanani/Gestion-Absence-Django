# Generated by Django 5.0.1 on 2024-01-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfe', '0005_alter_admin_options_alter_student_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
