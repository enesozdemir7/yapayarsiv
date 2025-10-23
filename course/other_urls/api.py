from django.urls import path, include
from course.default_views.api import HelpViewSet,HelpCommentsViewSet,BlogViewSet,BlogCommentsViewSet,CourseViewSet,NotificationsViewSet,NotificationShowApiView,basedSearch,blogLike,helpLike,blogCommentLike,helpCommentLike
from rest_framework.routers import DefaultRouter

app_name = "api"


router = DefaultRouter()
router.register(r'help', HelpViewSet)
router.register(r'help-comments', HelpCommentsViewSet)

router.register(r'blog', BlogViewSet)
router.register(r'blog-comments', BlogCommentsViewSet)

router.register(r'course', CourseViewSet)
router.register(r'notifications', NotificationsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('notification-show',NotificationShowApiView.as_view(),name="notification-show"),
    path('base-search/',basedSearch,name='base-search'),
    path('blog-like/',blogLike,name='blog-like'),
    path('blog-comment-like/',blogCommentLike,name='blog-comment-like'),

    path('help-like/',helpLike,name='help-like'),
    path('help-comment-like/',helpCommentLike,name='help-comment-like'),


]