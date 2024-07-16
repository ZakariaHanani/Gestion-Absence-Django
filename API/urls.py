from django.urls import path
from .views import signup, login, updateview

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('update/', updateview),
]