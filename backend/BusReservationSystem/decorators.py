from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def employee_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_employee:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def customer_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_customer:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
