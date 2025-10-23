from django.contrib import admin
from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('profil/', profile, name="profile"),
    path('parola-degistir/', changePasswordView, name="change-password"),
    path('favoriler/', favorites, name="favorites"),
    path('favori_sil/<int:id>/', delete_favorites, name="delete_favorites"),
    path('ayarlar/', settings, name="settings"),
    path('admin-panel/', admin_dashboard, name="dashboard"),
    path('kullanici-yonetimi/', manage_users, name="manage_users"),
    path('kullanici-duzenle/<int:id>/', update_user, name="update_user"),
    path('kullanici-blokla/<int:id>/', block_user, name="block_user"),
    path('kayit/', register, name="register"),
    path('giris/', user_login, name="login"),
    path('cikis/', user_logout, name="logout"),
]
