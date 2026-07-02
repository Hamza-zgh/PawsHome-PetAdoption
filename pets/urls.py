from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pet/<int:pet_id>/', views.pet_details, name='pet_details'),

    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add/', views.add_pet, name='add_pet'),
    path('dashboard/edit/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('dashboard/requests/<int:demand_id>/', views.manage_adoption, name='manage_adoption'),
]