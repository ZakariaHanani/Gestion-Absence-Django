from django import forms
from django.forms import TimeInput

from pfe.models import *

# forms.py in your Django app


class LoginForm(forms.Form):
    id = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Identifiant d\'Utilisateur'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )



class SeanceForm(forms.Form):

    Identifiant_Professeur  = forms.CharField(max_length=100, required=False, disabled=True)
    Nom = forms.CharField(max_length=100, required=False, disabled=True)
    Prenom = forms.CharField(max_length=100, required=False, disabled=True)
    HeureDebut = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}))
    HeureFin = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}))
    annee = forms.ModelChoiceField(queryset=Annee.objects.all(), empty_label="Select Annee")
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), empty_label="Select Filiere")
    matiere = forms.ModelChoiceField(queryset=Matiere.objects.all(), empty_label="Select Matiere")

