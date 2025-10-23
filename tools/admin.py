from django.contrib import admin
from .forms import ToolCreationForm, ToolChangeForm, ToolStarsForm
from django.utils.translation import gettext_lazy as _

from .models import Tool, ToolStars,ToolCategories2,ToolSubCategories
admin.site.register(ToolCategories2)
admin.site.register(ToolSubCategories)

class ToolStarsAdmin(admin.ModelAdmin):
    add_form = ToolStarsForm
    form = ToolStarsForm
    model = ToolStars
    list_display = (
            "user", "tool", "star",
            )
    list_filter = (
            "user", "tool", "star",
            )
    add_fieldsets = (
        (
            "Filter", {
                "classes": ("wide",),
                "fields": (
                    "user", "tool", "star",
                )
            }
        ),
    )
    search_fields = (
        "user", "tool", "star",
        )
    ordering = (
        "user", "tool", "star",
        )



class ToolAdmin(admin.ModelAdmin):
    add_form = ToolCreationForm
    form = ToolChangeForm
    model = Tool
    list_display = (
            "tool_name", "title",
             "fee", "product_url", "is_priority",
            "sponsored", "visible", "created_at",
            )
    list_filter = (
            "tool_name", "title",
            "subcategory", "fee", "product_url", "is_priority",
            "sponsored", "visible", "created_at",
            )
    fieldsets = (
        (
            "Tool Detail", {
                "fields": (
                    "tool_name", "title","banner", "fee", "visible",
                )
            }
        ),
        (
            "Category", {
                "fields": (
                    "subcategory",
                )
            }
        ),
        (
            "Sponsored & Priority", {
                "fields": (
                    "is_priority", "sponsored",
                )
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                "classes": ("wide",),
                "fields": (
                    "tool_name", "title", "subcategory","banner", "fee", "product_url",
                    "is_priority", "sponsored", "visible", "created_at",
                )
            }
        ),
    )
    search_fields = (
        "tool_name", "title","subcategory", "fee", "product_url",
        "is_priority", "sponsored", "visible", "created_at",
        )
    ordering = (
        "tool_name", "title", 
        )

admin.site.register(ToolStars, ToolStarsAdmin)
admin.site.register(Tool, ToolAdmin)
