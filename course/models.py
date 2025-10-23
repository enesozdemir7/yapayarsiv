from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.translation import gettext_lazy as _
import os
from django.core.validators import MaxValueValidator,MinValueValidator

def turkish_to_english(text):
    turkish_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
    
    for tr, en in turkish_chars.items():
        text = text.replace(tr, en)
    
    return text

class Category(models.Model):
    name = models.CharField(verbose_name='Kategori Adı',max_length=250)
    icon = models.ImageField(verbose_name='Kategori İkon',upload_to='course/kategori_logo')
    slug = models.SlugField(unique=True,blank=True,null=True,editable=False)
    index = models.IntegerField(default=1,verbose_name='Sıra no')
    ai_category = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.name)
            get_uuid_key = str(uuid.uuid4())[0:4]

            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(Category, self).save(*args, **kwargs)
    def get_blog_count(self):
        return Blog.objects.filter(category__in=[self]).count()
    class Meta:
        ordering = ['index']

    def __str__(self):
        return self.slug


class Blog(models.Model):

    banner = models.ImageField(upload_to='course/blog',blank=True,null=True)
    video_embed_link = models.CharField(verbose_name='embed video',blank=True,null=True)
    title = models.CharField(_("Başlık"), blank=False, max_length=255)

    author = models.ForeignKey("users.customuser", null=True, on_delete=models.SET_NULL, verbose_name=_('Yazar'))
    content = models.TextField(_("İçerik"))
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)
    slug = models.SlugField(unique=True,blank=True,null=True,editable=False)
    category = models.ManyToManyField(Category,blank=True,verbose_name=_("Alt Kategori"))
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.title)
            get_uuid_key = str(uuid.uuid4())[0:4]

            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(Blog, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _("Haber")
        verbose_name_plural = _("Haberler")
        ordering = ['-created_at']


class BlogComments(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.SET_NULL,null=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey("users.customuser",on_delete=models.SET_NULL,null=True)
    comment = models.CharField(max_length=500,verbose_name='Yorum')
    date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['date']


class FAQ(models.Model):
    question = models.CharField(verbose_name='Soru',max_length=250)
    reply = models.TextField(verbose_name='Cevap')
    index = models.IntegerField(default=1,verbose_name='Sıra no')

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['index']


class Course(models.Model):
    title = models.CharField(verbose_name='Kurs Başlığı')
    desc = models.CharField(verbose_name='Kurs Açıklaması')
    banner = models.ImageField(upload_to='course/courses')
    created_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey("users.customuser", null=True, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    active = models.BooleanField(default=True)

    def get_sections(self):
        return CourseSection.objects.filter(course=self)

    def user_start_count(self):
        return CompletedCourses.objects.filter(lesson__course_section__course=self.id).distinct("user").count()

    
    def get_first_section(self):
        return CourseSection.objects.filter(course=self).first() 

    def get_lesson_count(self):
        return CourseSectionLesson.objects.filter(course_section__id__in=list(CourseSection.objects.filter(course=self).values_list('id',flat=True))).count()


class CourseSection(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, verbose_name=_('Oluşturan'))
    name = models.CharField(verbose_name='Bölüm Adı')
    index = models.IntegerField(default=1,verbose_name='Sıra no')

    def get_lesson_count(self):
        return CourseSectionLesson.objects.filter(course_section=self).count()

    def get_lessons(self):
        return CourseSectionLesson.objects.filter(course_section=self)  
    
    def get_first_lesson(self):
        return CourseSectionLesson.objects.filter(course_section=self).first() 
        

    class Meta:
        ordering = ['index']

class CourseSectionLesson(models.Model):
    course_section = models.ForeignKey(CourseSection, null=True, on_delete=models.CASCADE, verbose_name=_('kurs bölüm'))
    title = models.CharField(max_length=250,verbose_name='Kurs Başlığı')
    content = models.TextField(_("İçerik"),blank=True,null=True)
    vimeo_embed_link = models.CharField(verbose_name='Vimeo Embed Link',blank=True,null=True)
    video_time = models.CharField(blank=True,null=True)
    index = models.IntegerField(default=1,verbose_name='Sıra no')

    class Meta:
        ordering = ['index']


class CompletedCourses(models.Model):

    user = models.ForeignKey("users.customuser", null=True, on_delete=models.SET_NULL, verbose_name=_('user'))
    lesson = models.ForeignKey(CourseSectionLesson, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class CourseProgress(models.Model):
    
    user = models.ForeignKey("users.customuser", null=True, on_delete=models.SET_NULL, verbose_name=_('user'))
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL, verbose_name=_('kurs'))
    lesson_list = models.JSONField(default=dict,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)



class SiteSettings(models.Model):

    title = models.CharField(verbose_name='Site AnaSayfa Başlığı')
    desc = models.CharField(verbose_name='Site Meta Açıklama')
    keywords = models.CharField(verbose_name='Site Meta Anahtar Kelimeler')
    fav_icon = models.FileField(verbose_name='Fav İcon',upload_to='course/site_images',blank=True,null=True)
    logo = models.ImageField(verbose_name='Site Logo',upload_to='course/site_images',blank=True,null=True)
    dark_logo = models.ImageField(verbose_name='Site Dark Logo',upload_to='course/site_images',blank=True,null=True)

    def fav_icon_name(self):
        if self.fav_icon:
            return os.path.basename(self.fav_icon.name)
        else:
            return 'dosya bulunamadı.'
        
    def logo_name(self):
        if self.logo:
            return os.path.basename(self.logo.name)
        else:
            return 'dosya bulunamadı.'

    def dark_logo_name(self):
        if self.dark_logo:
            return os.path.basename(self.dark_logo.name)
        else:
            return 'dosya bulunamadı.'


class Help(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.SET_NULL,null=True)
    title = models.CharField(verbose_name='Soru Başlığı')
    details =  models.CharField(verbose_name='Detaylar')
    date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)


    class Meta:
        ordering = ['-date']

class HelpComments(models.Model):
    help = models.ForeignKey(Help,on_delete=models.SET_NULL,null=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey("users.customuser",on_delete=models.SET_NULL,null=True)
    comment = models.CharField(max_length=500,verbose_name='Yorum')
    date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['date']


class Notifications(models.Model):
    title = models.CharField(verbose_name='Bildirim Başlığı')
    sender = models.CharField(default='Yapay Arşiv')
    link = models.CharField(blank=True,null=True)
    system = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def get_send_value(self):
        return NotificationsUsers.objects.filter(notification=self).count()

    def get_show_value(self):
        return NotificationsUsers.objects.filter(notification=self,showing=True).count()


class NotificationsUsers(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    notification = models.ForeignKey(Notifications,on_delete=models.CASCADE)
    showing = models.BooleanField(default=False)
    sound_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-notification__date']


class UserPayments(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    merchant_oid = models.CharField()
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(verbose_name='Tutar',default=0)
    status = models.BooleanField(default=None,blank=True,null=True)
    checked = models.BooleanField(default=False)
    coupon_code = models.CharField(default=None,blank=True,null=True)

    class Meta:
        ordering = ['-date']


class HomeSlider(models.Model):
    title = models.CharField(verbose_name='Bildirim Başlığı')
    desc = models.CharField(verbose_name='Kısa Açıklama')
    button_link = models.CharField(verbose_name='Buton Linki',blank=True,null=True)
    banner = models.ImageField(upload_to='course/slider')

    class Meta:
        ordering = ['-id']


class CouponCode(models.Model):
    code = models.CharField(verbose_name='Kupon Kodu')
    limit  = models.IntegerField(default=1,verbose_name='Kupon Limiti (Adet*)',validators=[MinValueValidator(1)])
    discount_percent = models.IntegerField(verbose_name='İndirim (%*)',validators=[MaxValueValidator(100)],blank=True,null=True)
    discount_amount = models.FloatField(verbose_name='İndirim (Tutar TL*)',blank=True,null=True)

    def __str__(self):

        return self.code

    class Meta:
        ordering = ['-id']

class UserCoupon(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    coupon = models.ForeignKey(CouponCode,on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

class UserBlogLikes(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)


class UserHelpLikes(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    post = models.ForeignKey(Help,on_delete=models.CASCADE)


class UserBlogCommentLikes(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    comment = models.ForeignKey(BlogComments,on_delete=models.CASCADE)

class UserHelpCommentLikes(models.Model):
    user = models.ForeignKey("users.customuser",on_delete=models.CASCADE)
    comment = models.ForeignKey(HelpComments,on_delete=models.CASCADE)