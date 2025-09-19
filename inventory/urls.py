from django.urls import path
from . import views

urlpatterns = [

    #CATEGORIES CRUD URLS
    path('category/create/', views.category_create, name='category_create'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/edit/<int:pk>/', views.category_update, name='category_update'),
    path('category/delete/<int:pk>', views.category_delete, name='category_delete'),
]
