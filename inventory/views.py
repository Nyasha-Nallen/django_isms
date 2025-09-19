from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.decorators import admin_required
from django.contrib import messages
from .models import Category, Product
from .forms import CategoryForm, ProductForm

# Create your views here.
#==========================
# CATEGORY CRUD VIEWS
#==========================
@login_required
@admin_required
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'inventory/category_list.html', context)

@login_required
@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, "Category created successfully")
            return redirect('category_list')
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'inventory/category_form.html', context)

@login_required
@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            cat = form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'inventory/category_form.html', context)

@login_required
@admin_required
def category_delete(request, pk):
    item = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('category_list')
    context = {
        'item': item,
        'type': 'Category'
    }
    return render(request, 'inventory/confirm_delete.html', context)