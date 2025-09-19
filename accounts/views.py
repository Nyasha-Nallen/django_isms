from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthForm
from .models import CustomUser

# Create your views here.
def register_staff(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_role = 'STAFF'
            user.save()
            messages.success(request, 'Your account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                #User Role Based Redirection
                if user.user_role == 'ADMIN':
                    return redirect("admin_dashboard")
                elif user.user_role == 'STAFF':
                    return redirect("staff_dashboard")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = CustomAuthForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

@login_required
def dashboard_view(request):
    user = request.user
    context={
        'user':user,
    }
    return render(request, 'accounts/dashboard.html', context)