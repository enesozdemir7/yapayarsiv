from django.urls import path
from course.default_views import user as userViews


app_name = "user"

urlpatterns = [
    path('paylasimlarim/',userViews.userBlogView,name='blog'),
    path('paylasimlarim/duzenle/<str:id>/',userViews.editUserBlogView,name='edit-blog'),
    path('paylasimlarim/sil/<str:id>/',userViews.deleteUserBlogView,name='delete-blog'),

    path('yardim-paylasimlarim/',userViews.userHelpView,name='help'),
    path('yardim-paylasimlarim/duzenle/<str:id>/',userViews.editUserHelpView,name='edit-help'),
    path('yardim-paylasimlarim/sil/<str:id>/',userViews.deleteUserHelpView,name='delete-help'),

    path('odemelerim/',userViews.userPaymentsView,name='payments'),

]

