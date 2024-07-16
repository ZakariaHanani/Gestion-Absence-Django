from django.urls import path
from pfe.views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('home',home_view, name='home'),
    path('teacher',teacher_view, name='teacher'),
    path('admin_dashboard',admin_view, name='admin'),
    path('seance/display/<int:seance_id>/', display_qr_code, name='display_qr_code'),
    path('logout', logout_view, name='logout'),
    path('admin/logout', logout_view, name='logout'),
    path('teacher_start_seance', teacher_satrt_seance, name='teacher_satrt_seance'),
    path('student_attendance', Student_attendance_view, name='student_attendance'),
    path('list_absence/', list_absence_view, name='list_absence_view'),
    path('seance/<int:seance_id>/', affiche_detail_seance_view, name='detail_seance'),

]