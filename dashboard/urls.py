from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/staff/", views.staff_dashboard, name="staff_dashboard"),
]
