from django.urls import path
from course.default_views import help as helpViews


app_name = "help"

urlpatterns = [
    path('',helpViews.helpListView,name='help-list'),

]

