from django.contrib import admin
from django.urls import path
from .views import *

app_name = "forum"

urlpatterns = [
    path('gonderiler/', all_post, name="all_posts"),
    path('gonderiler/more_post/', more_posts, name="more_posts"),
    #path('gonderiler/<int:id>/', post, name="post"),
    path('haberler/', all_news, name="all_news"),
    path('haberler/<str:slug>/', news, name="news"),
    path('iletisim/', contact, name="contact"),
    path('hakkinda/', about, name='about'),
    path('gizlilik-politikasi-ve-sorumluluk-reddi/', privacy, name='privacy'),
    path('kullanim-kosullari/', terms, name='terms'),
    path('iletisim-veri/<int:id>/', contact_data, name="contact_data"),
    path('haberleri-yonet/', manage_news, name="manage_news"),
    path('haber-ekle/', add_news, name="add_news"),
    path('haber-guncelle/<int:id>/', update_news, name="update_news"),
    path('haber-sil/<int:id>/', delete_news, name="delete_news"),
    path('gonderileri-yonet/', manage_posts, name="manage_posts"),
    path('gonderi-ekle/', add_post, name="add_post"),
    path('gunderi-guncelle/<int:id>/', update_post, name="update_post"),
    path('gonderi-sil/<int:id>/', delete_post, name="delete_post"),
    path('forum/', forum, name="forum"),
    path('forum/<int:id>/', category, name="forum_category"),
    path('forum/<int:category_id>/<int:subcategory_id>/', subcategory, name="forum_subcategory"),
    path('forum/<int:category_id>/<int:subcategory_id>/<int:thread_id>/', thread, name="forum_thread"),
    path('post-ajax-loadmore/', post_ajax_loadmore, name="post-ajax-loadmore"),
    #path('robots.txt/', robots, name="robots.txt", content_type='text/plain'),
]