from django.urls import path
from course.default_views import blog as blogViews


app_name = "blog"

urlpatterns = [
    path('',blogViews.blogListView,name='blog-list'),
    path('kategori/<str:slug>/',blogViews.catView,name='blog-category'),

]

