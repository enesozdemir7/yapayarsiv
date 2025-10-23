from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from course import views as courseViews
from course.default_views import basic_pages


urlpatterns = [
    path('',courseViews.indexView,name='index'),
    path('araclar/',basic_pages.toolsView,name='tools'),
    path('sss/',basic_pages.sssView,name='faq'),
    path('promptlar/',basic_pages.promptsView,name='prompts'),
    path('kategoriler/',basic_pages.categoryView,name='category'),
    path('ai-arac-kategorileri/',basic_pages.aiCategoryView,name='ai-tool-category'),
    path('bildirimler/',basic_pages.notificationsView,name='notifications'),
    path('katil/',courseViews.joinview,name='join'),
    path('giris/',courseViews.loginView,name='login'),
    path('kayit/',courseViews.registerView,name='register'),
    path('cikis/',courseViews.logoutView,name='logout'),
    path('teslimat-ve-iade-politikasi/',courseViews.deliveryandreturnView,name='delivery_and_return'),
    path('gizlilik-politikasi/',courseViews.privacypolicyView,name='privacy_policy'),
    path('odeme-hatasi/',courseViews.paymentErrorView,name='error-payment'),
    path('odeme-basarili/',courseViews.paymentSuccessView,name='successful-payment'),

    path('yonetim-paneli/',include("course.other_urls.management_urls")),
    path('kurslar/',include("course.other_urls.course_urls")),
    path('kullanici/',include("course.other_urls.user_urls")),
    path('yardim/',include("course.other_urls.help_urls")),
    path('hizli-ogren/',include("course.other_urls.blog_urls")),
    path('api/',include("course.other_urls.api")),
    path('paytr-callback/', paytrCallback, name="paytr-callback"),
    path('oauth/', include('social_django.urls', namespace='social')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)