from django.contrib import admin
from .forms import ( PostCreationForm, PostChangeForm, 
                    NewsCreationForm, NewsChangeForm, 
                    ForumCategoryCreationForm, ForumCategoryChangeForm,
                    ForumSubCategoryCreationForm, ForumSubCategoryChangeForm,
                    ForumThreadCreationForm, ForumThreadChangeForm )

from .models import ( Post, News, ForumCategory, 
                    ForumSubCategory, ForumThread )

from django.utils.translation import gettext_lazy as _


class ForumThreadyAdmin(admin.ModelAdmin):
    add_form = ForumThreadCreationForm
    form = ForumThreadChangeForm
    model = ForumThread
    list_display = ( "category", "subcategory", "user", "title", "body", "visible", "reported", )
    list_filter = ("category", "subcategory", "user", "title", "body", "visible", "reported", )
    fieldsets = (
        (
            "Thread Detail", {
                "fields": ("category", "subcategory", "user", "title", "body", "visible", "reported", )
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                    "classes": ("wide",),
                    "fields": ("category", "subcategory", "user", "thread_id", "title", "body", "visible", "reported", )
            }
        ),
    )
    search_fields = ("thread_id", "title", "body", "category", "subcategory", "user", "visible", "reported", )
    ordering = ("thread_id", "title", "body", "category", "subcategory", "user", "visible", "reported", )


class ForumCategoryAdmin(admin.ModelAdmin):
    add_form = ForumCategoryCreationForm
    form = ForumCategoryChangeForm
    model = ForumCategory
    list_display = ("category", "explanation", "visible", )
    list_filter = ("category",  "explanation", "visible", )
    fieldsets = (
        (
            "ForumCategory Detail", {
                "fields": ("category", "explanation", "visible", )
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                    "classes": ("wide",),
                    "fields": ("category_id", "category", "explanation", "visible", )
            }
        ),
    )
    search_fields = ("category_id", "category", "explanation", "visible", )
    ordering = ("category_id", "category", "explanation", "visible", )


class ForumSubCategoryAdmin(admin.ModelAdmin):
    add_form = ForumSubCategoryCreationForm
    form = ForumSubCategoryChangeForm
    model = ForumSubCategory
    list_display = ("subcategory_name", "category", "subcategory_explanation", "visible", )
    list_filter = ("subcategory_name", "category", "subcategory_explanation", "visible", )
    fieldsets = (
        (
            "ForumSubCategory Detail", {
                "fields": ("subcategory_name", "category", "subcategory_explanation", "visible", )
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                    "classes": ("wide",),
                    "fields": ("subcategory_id", "category", "subcategory_name", "subcategory_explanation", "visible", )
            }
        ),
    )
    search_fields = ("subcategory_id", "category", "subcategory_name", "subcategory_explanation", "visible", )
    ordering = ("subcategory_id", "category", "subcategory_name", "subcategory_explanation", "visible", )


class PostAdmin(admin.ModelAdmin):
    add_form = PostCreationForm
    form = PostChangeForm
    model = Post
    list_display = (
        "title","no" , "visible",
        )
    list_filter = (
       "title", "no", "visible",  "created_at",
        )
    fieldsets = (
        (
            "Post Detail", {
                "fields": ("title", "visible","no","url","thumbnail")
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                    "classes": ("wide",),
                    "fields": ("banner", "title","visible", )
            }
        ),
    )
    search_fields = (
       "banner", "title", "visible", "created_at",
        )
    ordering = (
        "title",
        )
    
class NewsAdmin(admin.ModelAdmin):
    add_form = NewsCreationForm
    form = NewsChangeForm
    model = News
    list_display = (
        "title", "owner", "sponsored", "visible", "created_at"
        )
    list_filter = (
        "title", "owner", "sponsored", "visible", "created_at"
        )
    fieldsets = (
        (
            "News Detail", {
                "fields": ("title", "desc", "banner", "body", "sponsored", "visible",)
            }
        ),
    )
    add_fieldsets = (
        (
            "Filter", {
                    "classes": ("wide",),
                    "fields": ("news_id", "title","body", "sponsored", "visible", "created_at",)
            }
        ),
    )
    search_fields = (
        "news_id", "title", "owner", "body", "sponsored", "visible", "created_at",
        )
    ordering = (
        "news_id","title", "owner",
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)  
   
admin.site.register(Post, PostAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(ForumCategory, ForumCategoryAdmin)
admin.site.register(ForumSubCategory, ForumSubCategoryAdmin)
admin.site.register(ForumThread, ForumThreadyAdmin)
