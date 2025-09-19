from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_role == "ADMIN":
            return view_func(request, *args, **kwargs)
        return redirect("staff_dashboard")
    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_role == "STAFF":
            return view_func(request, *args, **kwargs)
        return redirect("admin_dashboard")
    return wrapper
