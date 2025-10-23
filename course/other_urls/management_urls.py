from django.urls import path,include
from course.management import faq_views, management_views,blog_views,category_views,courses_views,settings_views,notifications_view,help_views
from course.management import comments_view,homeslider_views


app_name = "management"

urlpatterns = [
    path('',management_views.indexView,name='index'),
    path('odeme-kayitlari/',management_views.paymentsView,name='payments'),
    path('uyeler/',management_views.membersViews,name='members'),

    #ayarlar
    path('ayarlar/genel-ayarlar/',settings_views.generalSettingsView,name='general-settings'),

    path('yorumlar/blog/',comments_view.blogCommentsView,name='blog-comments'),
    path('yorumlar/blog/<str:id>/',comments_view.deleteBlogCommentView,name='delete-blog-comment'),
    path('yorumlar/yardim/',comments_view.helpCommentsView,name='help-comments'),
    path('yorumlar/yardim/<str:id>/',comments_view.deleteHelpCommentView,name='delete-help-comment'),



    #kurslar
    path('kurslar/',courses_views.courseView,name='course'),
    path('kurslar/duzenle/<str:id>/',courses_views.editCourseView,name='edit-course'),
    path('kurslar/sil/<str:id>/',courses_views.deleteCourseView,name='delete-course'),
    path('kurslar/kullanici-kurs-ilerlemeleri/',courses_views.memberCourseProgress,name='member-course-progress'),
    path('kurslar/kullanici-kurs-ilerlemeleri/<str:id>/',courses_views.memberCourseProgressDetail,name='member-course-progress-detail'),

    path('kurslar/yonet/<str:id>/',courses_views.manageCourseView,name='manage-course'),
    path('kurslar/yonet/bolum-yonet/<str:id>/',courses_views.manageSectionView,name='manage-section'),
    path('kurslar/yonet/bolum-yonet/<str:id>/',courses_views.manageSectionView,name='manage-section'),
    path('kurslar/yonet/bolum-yonet/ders-ekle/<str:id>/',courses_views.addLessonView,name='add-lesson'),
    path('kurslar/yonet/bolum-yonet/ders-duzenle/<str:id>/',courses_views.editLessonView,name='edit-lesson'),
    path('kurslar/yonet/bolum-yonet/ders-sil/<str:id>/',courses_views.deleteLessonView,name='delete-lesson'),

    path('kurslar/yonet/bolum-yonet/duzenle/<str:id>/',courses_views.editSectionView,name='edit-section'),
    path('kurslar/yonet/bolum-yonet/sil/<str:id>/',courses_views.deleteSectionView,name='delete-section'),

    path('kurslar/change-index-course-section/',courses_views.ajaxSaveCourseSectionOrderView,name='change-index-course-section'),
    path('kurslar/change-index-section-lesson/',courses_views.ajaxSaveSectionLessonOrderView,name='change-index-section-lesson'),
    
    #blog
    path('blog/',blog_views.blogView,name='blog'),
    path('blog/ekle/',blog_views.addBlogView,name='add-blog'),
    path('blog/duzenle/<str:id>/',blog_views.editBlogView,name='edit-blog'),
    path('blog/sil/<str:id>/',blog_views.deleteBlogView,name='delete-blog'),
    
    #yardım
    path('yardim-paylasimlari/',help_views.helpView,name='help'),
    path('yardim-paylasimlari/duzenle/<str:id>/',help_views.editHelpView,name='edit-help'),
    path('yardim-paylasimlari/sil/<str:id>/',help_views.deleteHelpView,name='delete-help'),
    
    #kategori
    path('kategoriler/',category_views.categoryView,name='category'),
    path('kategoriler/ai-arac-kategori/',category_views.aiToolCategoryView,name='ai-tool-category'),
    path('kategoriler/duzenle/<str:id>/',category_views.editCategoryView,name='edit-category'),
    path('kategoriler/sil/<str:id>/',category_views.deleteCategoryView,name='delete-category'),
    path('kategoriler/change-index-category/',category_views.ajaxSaveCategoryOrderView,name='change-index-category'),
    
    #slider+
    path('anasayfa-slider/',homeslider_views.homeSliderView,name='home-slider'),
    path('anasayfa-slider/duzenle/<str:id>/',homeslider_views.editSliderView,name='edit-home-slider'),
    path('anasayfa-slider/sil/<str:id>/',homeslider_views.deleteSliderView,name='delete-home-slider'),
    
    #bildirimler
    path('bildirimler/',notifications_view.notificationsView,name='notifications'),
    path('bildirimler/duzenle/<str:id>/',notifications_view.editNotificationsView,name='edit-notifications'),
    path('bildirimler/sil/<str:id>/',notifications_view.deleteNotificationsView,name='delete-notifications'),

    #SSS
    path('sss/',faq_views.faqView,name='faq'),
    path('sss/duzenle/<str:id>/',faq_views.editFaqView,name='edit-faq'),
    path('sss/sil/<str:id>/',faq_views.deleteFaqView,name='delete-faq'),
    path('kategoriler/change-index-faq/',faq_views.ajaxSaveFaqOrderView,name='change-index-faq'),

]

