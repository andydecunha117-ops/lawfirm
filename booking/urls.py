from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lawyers/', views.lawyers, name='lawyers'),
    path('book/<int:slot_id>/', views.book, name='book'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('reports/', views.reports, name='reports'),
    path('slots/', views.slots_by_date, name='slots_by_date'),
    path('make_booking/', views.make_booking, name='make_booking'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),


]
