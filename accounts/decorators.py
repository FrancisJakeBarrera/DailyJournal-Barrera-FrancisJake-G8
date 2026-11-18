from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                messages.error(request, "Access denied: You cannot view that dashboard.")
                return redirect('dashboard_redirect')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
