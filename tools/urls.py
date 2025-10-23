from django.contrib import admin
from django.urls import path
from .views import *

app_name = "tools"

urlpatterns = [
    #path('kategoriler/', categories, name="categories"),
    path('arac/<str:slug>', tool, name="tool"),
    path('arac/arac-kategori/<str:cat_id>/', get_sub_cats, name="get_sub_cat"),
    path('favorilere-ekle/<str:slug>/', add_favorited, name="add_favorited"),
    path('favori-kaldir/<int:fav_id>/', remove_favorited, name="remove_favorited"),

    path('degerlendir/<str:slug>/<int:rating>/', rate, name="rate"),
    path('araclari-yonet/', manage_tools, name="manage_tools"),
    path('arac-ekle/', add_tool, name="add_tool"),
    path('arac-guncelle/<str:slug>/', update_tool, name="update_tool"),
    path('arac-sil/<str:slug>/', delete_tool, name="delete_tool"),
    path('sponsorluklari-yonet/', manage_ads, name="manage_ads"),
    path('reklam-sil/<int:id>/', delete_ad, name="delete_ad"),
    path('start_app/', start_app, name="start_app"),
    path('tool-ajax-loadmore/', tool_ajax_loadmore, name="tool-ajax-loadmore"),

]
