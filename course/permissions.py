from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect


class CustomPermission(BasePermission):


    def __init__(self,course='course'):
        self.course = course

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.course_user 

def course_custom_permission(code_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            custom_permission = CustomPermission(code_name)
            if not custom_permission.has_permission(request, None) and request.user.is_superuser != True:
                return redirect('join')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator