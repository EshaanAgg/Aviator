from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.flight_show, name='flight_show'),
    path('book/<int:flight_id>', views.book_flight, name='booking'),
    path('mybookings/', views.my_bookings, name='my_bookings'),
    path('', views.home_page, name='home_page'),
    path('add_flight/', views.create_flight, name='create_flight'),
]
