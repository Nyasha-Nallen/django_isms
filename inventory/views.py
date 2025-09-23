from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.decorators import admin_required
from django.contrib import messages
from .models import Category, Product, StockEntry, StockEntryItem, SaleTransaction, SaleItem
from .forms import CategoryForm, ProductForm, StockReceiptForm, StockReceiptItemFormSet, StockReceiptItemForm, SaleItemForm, SaleItemFormSet, SaleTransactionForm

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


#==========================
# PRODUCT CRUD VIEWS
#==========================
@login_required
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'inventory/product_list.html', context)

@login_required
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, "Product created successfully")
            return redirect('product_list')
    else:
        form = ProductForm()
    context = {
        'form':form,
    }
    return render(request, 'inventory/product_form.html', context)

@login_required
@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            prod = form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'inventory/product_form.html', context)

@login_required
@admin_required
def product_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('product_list')
    context = {
        'item': item,
        'type': 'Product'
    }
    return render(request, 'inventory/confirm_delete.html', context)

#==========================
# MULTI-ITEM STOCK RECEIPT 
#==========================
@login_required
def stock_receipt_create(request):
    if request.method == "POST":
        form = StockReceiptForm(request.POST)
        formset = StockReceiptItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            receipt = form.save(commit=False)
            receipt.received_by = request.user
            receipt.save()
            items = formset.save(commit=False)
            for item in items:
                item.receipt = receipt
                item.save()
            messages.success(request, "Stock received successfully.")
            return redirect("product_list")
    else:
        form = StockReceiptForm()
        formset = StockReceiptItemFormSet()
    context = {
        "form": form,
        "formset": formset
    }
    return render(request, "inventory/stock_receive_form.html", context)

#===================
# MULTI-ITEM SALE
#===================
@login_required
def sale_transaction_create(request):
    if request.method == "POST":
        form = SaleTransactionForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.sold_by = request.user
            sale.save()
            items = formset.save(commit=False)
            try:
                for item in items:
                    item.sale = sale
                    item.save()
                # After saving all items, update the sale total
                sale.update_total()
                messages.success(request, "Sale recorded successfully.")
                return redirect("product_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = SaleTransactionForm()
        formset = SaleItemFormSet()
    return render(request, "inventory/sale_transaction_form.html", {"form": form, "formset": formset})