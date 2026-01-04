from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Note, Folder
from .forms import NoteForm, FolderForm

@login_required(login_url='login')
def notes_home(request):
    # Get filter parameters
    folder_id = request.GET.get('folder')
    time_filter = request.GET.get('filter', 'all')
    
    # Base query
    notes = Note.objects.filter(user=request.user)
    
    # Apply folder filter
    if folder_id:
        notes = notes.filter(folder_id=folder_id)
    today = timezone.now().date()
    from datetime import datetime, timedelta
    today = timezone.now().date()
    
    if time_filter == 'today':
        notes = notes.filter(created_at__date=today)
    elif time_filter == 'week':
        week_ago = today - timedelta(days=7)
        notes = notes.filter(created_at__date__gte=week_ago)
    elif time_filter == 'month':
        month_ago = today - timedelta(days=30)
        notes = notes.filter(created_at__date__gte=month_ago)
    
    # Get folders with note counts
    folders = Folder.objects.filter(user=request.user).annotate(
        note_count=Count('notes')
    )
    
    context = {
        'notes': notes,
        'folders': folders,
        'active_filter': time_filter,
        'active_folder': folder_id,
    }
    
    return render(request, 'notes/notes_home.html', context)


@login_required(login_url='login')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.user, request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('notes_home')
    else:
        form = NoteForm(request.user)
    
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})


@login_required(login_url='login')
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.user, request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('notes_home')
    else:
        form = NoteForm(request.user, instance=note)
    
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Edit', 'note': note})


@login_required(login_url='login')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes_home')
    
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


@login_required(login_url='login')
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('notes_home')


@login_required(login_url='login')
def folder_create(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, 'Folder created successfully!')
            return redirect('notes_home')
    else:
        form = FolderForm()
    
    return render(request, 'notes/folder_form.html', {'form': form})


@login_required(login_url='login')
def folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        folder.delete()
        messages.success(request, 'Folder deleted successfully!')
        return redirect('notes_home')
    
    return render(request, 'notes/folder_confirm_delete.html', {'folder': folder})
