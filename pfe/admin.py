from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

class StudentManagaer(admin.ModelAdmin):
    search_fields =['id']
    list_display =['fname','lname','Identifiant_Filiere','email']
    list_filter = ['Identifiant_Filiere']
    
class TeacherManagaer(admin.ModelAdmin):
    search_fields =['fname','lname','Identifiant_Filiere']
    list_display =['fname', 'lname','email']
    
class SeanceManager(admin.ModelAdmin):
    list_display =['Nom', 'Identifiant_Matiere', 'DateSeance', 'HeureDebut', 'HeureFin', 'Identifiant_Professeur']
    list_filter = ['Identifiant_Matiere']
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True
  
    def has_add_permission(self, request): 
        return False
    
class AttendanceManager(admin.ModelAdmin):
    list_display =['Identifiant_Seance', 'Identifiant_Etudiant', 'Status']
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True
  
    def has_add_permission(self, request): 
        return False   
 
class MatiereManager(admin.ModelAdmin):
    list_display =['Identifiant_Filiere', 'Nom']
    list_filter = ['Identifiant_Filiere']
    
class AdminManager(admin.ModelAdmin):
    list_display =['is_superuser','email','is_active', 'is_staff', 'id', 'fname', 'lname', 'user_type']
    
        
     
    
# Register your models here.
admin.site.register(Admin,AdminManager)
admin.site.register(Filiere)
admin.site.register(Matiere,MatiereManager)
admin.site.register(Annee)
admin.site.register(Student,StudentManagaer)
admin.site.register(Teacher,TeacherManagaer)
admin.site.register(Seance,SeanceManager)
admin.site.register(Attendance,AttendanceManager)
admin.site.site_header = 'Espace Administratif' 
admin.site.site_title ='Espace Administratif'

