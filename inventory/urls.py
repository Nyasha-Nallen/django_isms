from django.urls import path
from . import views

urlpatterns = [

    #CATEGORIES CRUD URLS
    path('category/create/', views.category_create, name='category_create'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/edit/<int:pk>/', views.category_update, name='category_update'),
    path('category/delete/<int:pk>', views.category_delete, name='category_delete'),

    #PRODUCT CRUD URLS
    path('product/create/', views. product_create, name='product_create'),
    path('product/list/', views. product_list, name='product_list'),
    path('product/edit/<int:pk>/', views.product_update, name='product_update'),
    path('product/delete/<int:pk>', views.product_delete, name='product_delete'),

    #RECEIVE NEW STOCK URLS
    path("stock/receipt/", views.stock_receipt_create, name="stock_receipt_create"),
    
    #MAKE A SALE 
    path("sales/transaction/", views.sale_transaction_create, name="sale_transaction_create"),
]
