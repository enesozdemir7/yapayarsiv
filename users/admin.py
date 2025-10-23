from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username","email", "name", "surname",  "blocked", "is_verified", "editor", "is_staff", "is_active",)
    list_filter = ("blocked", "verified", "editor", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username","email", "password","name", "surname", "biography")}),
        ("Permissions", {"fields": ("blocked", "verified", "editor", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username","email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("username","email", "name", "surname", "verified", "editor", "blocked",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)