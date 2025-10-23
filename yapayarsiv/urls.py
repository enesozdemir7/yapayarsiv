from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from tools import views as tools_views
from django.contrib.auth import views as auth_views
from users.views import token_send,success,verify
from django.views.generic import TemplateView
from forum.feed import NewsFeed
from .sitemaps import StaticPagesSitemap,NewsSiteMap,ToolSiteMap,ToolCategorySiteMap,ToolSubCategorySiteMap
from django.contrib.sitemaps import views as sitemaps_views
from course.views import paytrCallback

from django.contrib.sites.models import Site

try:

    site = Site.objects.get_current()
    site.domain = 'yapayarsiv.com'
    site.save()
except:
    pass

sitemaps = {"static_pages": StaticPagesSitemap, "news_sitemap": NewsSiteMap, "tool_sitemap": ToolSiteMap, "tool_category_sitemap": ToolCategorySiteMap,"tool_subcategory_sitemap": ToolSubCategorySiteMap}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', tools_views.index, name="index"),
    path(
        "sitemap.xml",
        sitemaps_views.index,
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
        name="sitemap-index",
    ),
    path(
        "sitemap-<section>.xml",
        sitemaps_views.sitemap,
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),

    path('arac-kategori/<str:category>/', tools_views.index_category, name="index_category"),
    path('arac-kategori/<str:category>/<str:sub_category>/', tools_views.index_category, name="index_sub_category"),
    path('more/', tools_views.more_tools, name="more"),
    path('feed/', NewsFeed(), name='feed'),
    path('robots.txt/',TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('ads.txt/',TemplateView.as_view(template_name="ads.txt", content_type='text/plain')),
    path("araclar/", include("tools.urls")),
    path("", include("forum.urls")),
    path("kullanici/", include("users.urls")),

    path('parola-sifirla/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('parola-sifirla/tamamlandi/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('parola-sifirla/onay/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('parola-sifirla/basarili/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('token/gonderildi/' , token_send , name='token_send'),
    path('email-onay/basarili/' , success, name ='success'),
    path('email-onay/onay/<str:mail_token>/' , verify ,name = "verify"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
