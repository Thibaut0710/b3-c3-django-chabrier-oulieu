from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation', views.reservation, name='reservation'),
    path('ecoles-reservations', views.ecolesReservations, name='ecolesReservations'),
    path('horaires', views.horaires, name='horaires'),
    path('user-panel', views.userPanel, name='userPanel'),
    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('remove-reservation/<int:id>', views.removeReservation, name='removeReservation'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
]
