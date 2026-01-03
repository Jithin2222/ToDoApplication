from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')   
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('profile')
    else:
        form = RegisterForm()  
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('profile')
    else:
        form = LoginForm()  
    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')



@login_required(login_url='login')
def profile_view(request):
    # Get user statistics
    stats = request.user.profile.get_task_stats()
    # Get recent tasks
    recent_tasks = request.user.tasks.all()[:5]
    # Get tasks created this week
    week_ago = timezone.now() - timedelta(days=7)
    tasks_this_week = request.user.tasks.filter(created_at__gte=week_ago).count()
    # Get completed tasks this week
    completed_this_week = request.user.tasks.filter(
        completed=True, 
        updated_at__gte=week_ago
    ).count()
    context = {
        'stats': stats,
        'recent_tasks': recent_tasks,
        'tasks_this_week': tasks_this_week,
        'completed_this_week': completed_this_week,
    }   
    return render(request, 'accounts/profile.html', context)



@login_required(login_url='login')
def profile_edit_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    } 
    return render(request, 'accounts/profile_edit.html', context)

