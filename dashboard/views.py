from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, staff_required

# Create your views here.
@login_required
@admin_required
def admin_dashboard(request):
    user = request.user
    context={
        'user':user,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@staff_required
def staff_dashboard(request):
    user = request.user
    context={
        'user':user,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)