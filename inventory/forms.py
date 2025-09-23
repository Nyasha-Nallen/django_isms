from django import forms
from django.forms import inlineformset_factory
from .models import Product, Category, StockEntry, StockEntryItem, SaleTransaction, SaleItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "quantity", "price"]


class StockReceiptForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = []  


class StockReceiptItemForm(forms.ModelForm):
    class Meta:
        model = StockEntryItem
        fields = ["product", "quantity"]


StockReceiptItemFormSet = inlineformset_factory(
    StockEntry, StockEntryItem, form=StockReceiptItemForm, extra=3, can_delete=False
)


class SaleTransactionForm(forms.ModelForm):
    class Meta:
        model = SaleTransaction
        fields = []


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity"]


SaleItemFormSet = inlineformset_factory(
    SaleTransaction, SaleItem, form=SaleItemForm, extra=3, can_delete=False
)