from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_application, name='submit_application'),
    path('accept/', views.accept_application, name='accept_application'),
    path('reject/', views.reject_application, name='reject_application'),
]
