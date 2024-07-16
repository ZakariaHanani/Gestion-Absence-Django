import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, id, password, **extra_fields):
        if not id :
            raise ValueError('vous anvez pas saisir un id')
        user = self.model(id = id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id = None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, password, **extra_fields)

    def create_superuser(self, id = None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self._create_user(id, password, **extra_fields)
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

class User(AbstractUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    ]
    username = None

    first_name = None
    last_name = None
    date_joined =  None
    last_login = None
    id = models.CharField(max_length =100, primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'id'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'Nom complet: {self.fname} {self.lname}  id: {self.id}'


class Annee(models.Model):
    Identifiant_Annee = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=50)

    def __str__(self):
        return self.Nom

class Filiere(models.Model):
    Identifiant_Filiere = models.AutoField(primary_key=True)
    Identifiant_Annee = models.ForeignKey('Annee', on_delete=models.CASCADE)
    Nom = models.CharField(max_length=50)

    def __str__(self):
        return self.Nom





class Student(User):
    Identifiant_Filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.lname} - Student"

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


# Admin Model
class Admin(User):

    def __str__(self):
        return self.lname
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


# Teacher Model
class Teacher(User):
    def __str__(self):
        return self.lname
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'



class Matiere(models.Model):
    Identifiant_Matiere = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=50)
    Identifiant_Filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nom

class Seance(models.Model):
    Identifiant_Seance = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=50)
    DateSeance = models.DateField(auto_now=True)
    HeureDebut = models.TimeField()
    HeureFin = models.TimeField()
    Identifiant_Professeur = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Identifiant_Matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"identifiant seance: {self.Identifiant_Seance} "


    def GenerateQRCode(self, data):
        import os
        import random
        import qrcode

        randomNum = random.randint(0, 100000)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=25,
            border=1.5,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = f'qrcodes/{randomNum}.png'
        file_path = os.path.join('pfe/static/', filename)  # Full file path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        img.save(file_path)

        return filename  # Return the relative path from static


class Attendance(models.Model):
    Identifiant_Attendance = models.AutoField(primary_key=True)
    Identifiant_Etudiant = models.ForeignKey(Student, on_delete=models.CASCADE)
    Identifiant_Seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    Status = models.CharField(max_length=20, default='Absent(e)')

    def seance_diagramme(self, seance_id):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import os
        from django.conf import settings

        count_absent = int(Attendance.objects.filter(Status="Absent(e)", Identifiant_Seance=seance_id).count())
        count_present = int(Attendance.objects.filter(Status="Present(e)", Identifiant_Seance=seance_id).count())
        colors = ['#ff9999', '#66b3ff']
        pers = [count_absent, count_present]
        status_etud = ["Absence", "Presence"]
        img_rel_path = f"graph/{seance_id}.png"
        file_path = os.path.join(settings.BASE_DIR, 'pfe', 'static', img_rel_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plt.pie(pers, labels=status_etud, colors=colors, autopct='%1.2f%%')
        plt.savefig(file_path)
        plt.close()
        return img_rel_path

    def __str__(self):
        return f"seance: {self.Identifiant_Seance}, Element: {self.Identifiant_Attendance}"




