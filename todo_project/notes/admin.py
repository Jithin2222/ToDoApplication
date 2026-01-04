from django.contrib import admin
from .models import Note, Folder

# Register your models here.

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['created_at', 'color']
    search_fields = ['name', 'user__username']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'folder', 'is_pinned', 'created_at']
    list_filter = ['is_pinned', 'created_at', 'folder']
    search_fields = ['title', 'content', 'user__username']