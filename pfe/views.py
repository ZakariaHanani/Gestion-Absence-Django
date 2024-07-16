
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect



# views.py

from django.shortcuts import render



def login_view(request):
    from pfe.forms import LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            password = form.cleaned_data.get('password')
            user = authenticate(request, id=id, password=password)  # Use username=id
            print(password)
            if user:
                login(request, user)
                request.session['fname'] = user.fname
                request.session['lname'] = user.lname

                if user.user_type == 'teacher':
                    return redirect('teacher')
                elif user.user_type == 'admin':
                    return redirect('admin')
            else:
                messages.error(request, "Invalid ID or password.")
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})


@login_required(login_url='')
def teacher_view(request):
    fname = request.session.get('fname')
    lname = request.session.get('lname')
    print(request.session)
    print(lname)
    print(fname)
    username = f"{fname} {lname}"
    context = {"username": username}

    return render(request, 'teacher.html', context)



@login_required(login_url='')
def display_qr_code(request, seance_id):
    from pfe.models import Seance
    import json
    from django.core.serializers import serialize
    seance = Seance()
    seance_data = Seance.objects.get(Identifiant_Seance=seance_id)
    json_data_str = serialize('json', [seance_data])

    json_data = json.loads(json_data_str)
    data = json_data[0]["pk"]
    print(data)
    filename = seance.GenerateQRCode(data)
    context = {'filename': filename}
    return render(request, 'display_qr_code.html', context)


@login_required(login_url='')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def home_view(request):
    return render(request, 'index.html')

from pfe.models import Filiere, Matiere
from pfe.models import Annee
@login_required(login_url='')
def admin_view(request):
    Identifiant_annees = Annee.objects.values_list('Identifiant_Annee', flat=True).distinct()
    annees = Annee.objects.all()
    tab_data = []

    for annee in annees:
        filieres = Filiere.objects.filter(Identifiant_Annee=annee.Identifiant_Annee)
        nom_filieres = filieres.values_list('Nom', flat=True)
        nom_annee = annee.Nom

        for nom_filiere in nom_filieres:
            data = {"nom_filiere": nom_filiere, "nom_annee": nom_annee}
            tab_data.append(data)


    lname = request.session.get("lname")
    fname = request.session.get("fname")
    name = f"{lname} {fname}"
    context = {'tab_data': tab_data, "name":name}

    print(name)

    return render(request, 'admin.html', context)

@login_required(login_url='')
def teacher_satrt_seance(request):
    from pfe.models import Seance, Attendance, Student, Filiere
    from pfe.forms import SeanceForm
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        print('post')
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = Seance(
                Identifiant_Professeur=request.user.teacher,  # Assuming the user has a related 'teacher' object
                Nom=form.cleaned_data['Nom'],
                HeureDebut=form.cleaned_data['HeureDebut'],
                HeureFin=form.cleaned_data['HeureFin'],
                Identifiant_Filiere=form.cleaned_data['filiere'],  # Directly use the returned object
                Identifiant_Annee=form.cleaned_data['annee'],      # Directly use the returned object
                Identifiant_Matiere=form.cleaned_data['matiere']   # Directly use the returned object
            )
            seance.save()
            filiere = form.cleaned_data['filiere']
            students = Student.objects.filter(Identifiant_Filiere=filiere)
            for student in students:
                attendance = Attendance(
                    Identifiant_Etudiant= student,
                    Identifiant_Seance = seance,
                    Status= 'absent(e)',
                )

                attendance.save()

            return redirect('display_qr_code', seance_id=seance.Identifiant_Seance )
        else:
            print(form.errors)
    else:
        user = request.user
        form = SeanceForm(initial={
            'Identifiant_Professeur': user.id,  # This value won't be used in POST, it's just for display
            'Nom': user.lname,  # Assuming last_name is the field to use
            'Prenom': user.fname , # Assuming first_name is the field to use
        })
    return render(request, 'teacher_start_seance.html', {'form': form})

@login_required(login_url='')
def Student_attendance_view(request):
    from pfe.models import Seance, Matiere, Filiere, Annee
    # Assuming Identifiant_Professeur is a foreign key to the User model in the Seance model.
    Identifiant_seance = Seance.objects.filter(Identifiant_Professeur=request.user.pk).last()
    seances = Seance.objects.filter(Identifiant_Professeur=request.user.pk).prefetch_related('Identifiant_Matiere__Identifiant_Filiere__Identifiant_Annee')

    if seances.exists():
        # Constructing a list of dictionaries, each containing seance information and related filiere and annee names
        data_with_names = []
        for seance in seances:
            matiere = seance.Identifiant_Matiere
            filiere = matiere.Identifiant_Filiere
            annee = filiere.Identifiant_Annee
            data_with_names.append({
                'seance': seance,
                'matiere': matiere.Nom,
                'filiere_name': filiere.Nom,
                'annee_name': annee.Nom
            })
        context = {'data': data_with_names}
        return render(request, 'list_absence.html', context)
    else:
        context = {'isEmpty': True}
        return render(request, 'student_attendance.html', context)

@login_required(login_url='')
def list_absence_view(request):
    filiere_name = request.GET.get('filiere_name')
    annee_name = request.GET.get('nom_annee')

    Identifiant_annee = Annee.objects.get(Nom=annee_name)
    Identifiant_filiere = Filiere.objects.get(Nom=filiere_name, Identifiant_Annee=Identifiant_annee)

    Identifiant_matiere = Matiere.objects.filter(Identifiant_Filiere=Identifiant_filiere)
    print("***********************\n**********************\n***********")
    print(annee_name)
    print(filiere_name)

    data = Seance.objects.filter(Identifiant_Matiere__in=Identifiant_matiere)
    context = {'data': data, 'filiere_name': filiere_name, 'annee_name': annee_name}

    return render(request, 'list_absence.html', context)


from django.shortcuts import get_object_or_404, render
from .models import Seance, Attendance

@login_required(login_url='')
def affiche_detail_seance_view(request, seance_id):
    import matplotlib
    matplotlib.use('Agg')
    from pfe.models import Student
    seance = get_object_or_404(Seance, Identifiant_Seance=seance_id)
    matiere = seance.Identifiant_Matiere
    filiere = matiere.Identifiant_Filiere
    annee = filiere.Identifiant_Annee
    student = Student.objects.all()
    attendances = Attendance.objects.filter(Identifiant_Seance=seance_id)
    attendance = Attendance()
    img_rel_path = attendance.seance_diagramme(seance_id)


    context = {
        'seance': seance,
        'attendances': attendances,
        'student': student,
        'img_path': img_rel_path ,
        'filiere' : filiere,
        'annee' : annee
    }
    return render(request, 'affiche_liste_absence.html', context)




