from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
from .decorators import role_required
from .models import CustomUser

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'member'
            user.save()
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard_redirect')
        messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def dashboard_redirect_view(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('member_dashboard')

@login_required
@role_required(['admin'])
def admin_dashboard_view(request):
    return render(request, 'accounts/admin_dashboard.html', {
        'total_users': CustomUser.objects.count(),
        'members': CustomUser.objects.filter(role='member'),
    })

@login_required
@role_required(['member'])
def member_dashboard_view(request):
    return render(request, 'accounts/member_dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user_obj': request.user})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})