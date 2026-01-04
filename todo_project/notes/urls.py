from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_home, name='notes_home'),
    path('create/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('pin/<int:pk>/', views.note_toggle_pin, name='note_toggle_pin'),
    path('folder/create/', views.folder_create, name='folder_create'),
    path('folder/delete/<int:pk>/', views.folder_delete, name='folder_delete'),
]