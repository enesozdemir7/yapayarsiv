from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from course.models import CourseSectionLesson,CompletedCourses

from users.managers import CustomUserManager

from django import template

register = template.Library()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True, verbose_name="Kullanıcı adı",default="1")
    user_id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True,null=True)
    biography = models.TextField(max_length=500, blank=True)
    #job = models.CharField(blank=True)
    #city = models.CharField(blank=True)
    github = models.CharField(blank=True)
    instagram = models.CharField(blank=True)
    website = models.CharField(blank=True)
    verified = models.BooleanField(default=False)
    editor = models.BooleanField(default=False)
    last_login = models.DateField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    blocked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    mail_token = models.CharField(max_length=100,default=None,blank=True,null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    course_user = models.BooleanField(default=False)
    course_joined = models.DateTimeField(default=None,blank=True,null=True)
    objects = CustomUserManager()

    def full_name(self):
        return f"{self.name} {self.surname}"

    def get_course_progress(self,course_id):
        get_progress_max = CourseSectionLesson.objects.filter(course_section__course__id=course_id).count()
        current_progress = CompletedCourses.objects.filter(lesson__course_section__course__id=course_id,user=self).count()

        try:
            current_progress = (current_progress / get_progress_max) * 100
        except:
            current_progress = 0
        
        return current_progress

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("Kullanıcı")
        verbose_name_plural = _("Kullanıcılar")
        