from django.urls import path
from course.default_views import course as courseViews


app_name = "course"

urlpatterns = [
    path('',courseViews.courseListView,name='course-list'),
    path('<str:id>/',courseViews.coursePromotionView,name='course-promotion'),
    path('<str:id>/icerik/',courseViews.courseDetailView,name='course-detail'),

    path('api/ders-icerik-api/',courseViews.getLessonDetailView,name='lesson-detail-api'),

]

