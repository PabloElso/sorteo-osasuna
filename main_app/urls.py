from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Add other app-specific URLs here
]