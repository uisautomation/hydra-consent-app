from django.urls import path

from . import views

urlpatterns = [
    path('healthz', views.healthz),
    path('consent/', views.consent, name='consent'),
]
