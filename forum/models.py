from django.db import models
from django.utils import timezone
from users.models import CustomUser
from tools.models import Tool
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image
from django.utils.text import slugify
import uuid
## Post

def turkish_to_english(text):
    turkish_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
    
    for tr, en in turkish_chars.items():
        text = text.replace(tr, en)
    
    return text

def crop_image(instance, filename):
    filename = filename.split(".")
    filename = filename[-1]

    def save_cropped_image(cropped_image, filename):
        cropped_image.convert('RGB').save(filename, 'WEBP', quality=50)

    return save_cropped_image



class Post(models.Model):
    post_id = models.AutoField(primary_key=True, unique=True)
    #tool = models.ForeignKey(Tool, null=True, on_delete=models.SET_NULL, verbose_name=_("Araç"))
    no = models.CharField(_("Numara"),blank=True,null=True)
    thumbnail = models.ImageField(_("Küçük Resim"), upload_to=settings.MEDIA_THUMBNAILS_URL)
    title = models.CharField(_("Başlık"), blank=False)
    url = models.CharField(_("URL"))
    #body = RichTextField(_("İçerik"), blank=False)
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Gönderi")
        verbose_name_plural = _("Gönderiler")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.thumbnail.path)

        width, height = image.size

        min_size = min(width, height)

        left = (width - min_size) / 2
        top = (height - min_size) / 2
        right = (width + min_size) / 2
        bottom = (height + min_size) / 2

        cropped_image = image.crop((left, top, right, bottom))

        save_cropped_image = crop_image(self, self.thumbnail.name)
        save_cropped_image(cropped_image, self.thumbnail.path)


class PostsComment(models.Model):
    posts_comment_id = models.AutoField(primary_key=True, unique=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Gönderi ID'si"))
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name=_('Yorum sahibi'))
    body = RichTextField(_("İçerik"), blank=False)
    reported = models.BooleanField(_("Şikayet edildi mi?"), default=False)
    blocked = models.BooleanField(_("Engellendi mi?"), default=False)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)

    def __str__(self):
        return self.posts_comment_id
    
    class Meta:
        verbose_name = _("Gönderi Yorumu")
        verbose_name_plural = _("Gönderi Yorumları")

## News

class News(models.Model):
    news_id = models.AutoField(primary_key=True, unique=True)
    #tool = models.ForeignKey(Tool, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Araç ID'si"))
    banner = models.ImageField(upload_to='news_banners')
    title = models.CharField(_("Başlık"), blank=False)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name=_('Yazar'))
    body = RichTextField(_("İçerik"), blank=False)
    desc = models.CharField(_("Açıklama"))
    sponsored = models.BooleanField(_("Sponsorlu mu?"), default=False)
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)
    slug = models.SlugField(unique=True,blank=True,null=True,editable=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse("forum:news", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.title)
            get_uuid_key = str(uuid.uuid4())[0:4]

            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(News, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _("Haber")
        verbose_name_plural = _("Haberler")
        ordering = ['-created_at']

class NewsComment(models.Model):
    news_comment_id = models.AutoField(primary_key=True, unique=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name=_("Haber ID'si"))
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name=_('Yorum sahibi'))
    body = RichTextField(_("İçerik"), blank=False)
    reported = models.BooleanField(_("Şikayet edildi mi?"), default=False)
    blocked = models.BooleanField(_("Engellendi edildi mi?"), default=False)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)

    def __str__(self):
        return self.news_comment_id
    
    class Meta:
        verbose_name = _("Haber Yorumu")
        verbose_name_plural = _("Haber Yorumları")


class Useful(models.Model):
    comment = models.ForeignKey(PostsComment, on_delete=models.CASCADE, verbose_name=_('Yorum'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Kullanıcı'))
    useful = models.IntegerField(_("Yararlı"), default=0)
    not_useful = models.IntegerField(_("Yararlı Değil"), default=0)

    class Meta:
        verbose_name = _("Yararlı")
        verbose_name_plural = _("Yararlı")


## Forum ##

class ForumCategoryNames(models.TextChoices): 
    QUESTION_ANSWER = "Soru-Cevap", _("Soru-Cevap")
    ONLINE_CONTENT = "Online İçerik", _("Online İçerik")
    TECHNOLOGY = "Teknoloji", _("Teknoloji")
    TESTING_AND_PURCHASING = "Test ve Satın Alma", _("Test ve Satın Alma")
    HARDWARE = "Donanım", _("Donanım")
    SOFTWARE_DEVELOPMENT = "Yazılım Geliştirme", _("Yazılım Geliştirme")
    DATA_SCIENCE = "Veri Bilimi", _("Veri Bilimi")
    AI_GENERATION = "Yapay Zeka Üretimi", _("Yapay Zeka Üretimi")
    GAMES = "Oyunlar", _("Oyunlar")
    FEEDBACK = "Geri Bildirim", _("Geri Bildirim")
    OPEN_FORUM = "Serbest Kürsü", _("Serbest Kürsü")

class ForumCategory(models.Model):
    category_id = models.AutoField(primary_key=True, unique=True)
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    explanation = models.CharField(_("Açıklama"), blank=False)
    category = models.CharField(
        _("Kategori"),
        choices=ForumCategoryNames.choices,
        unique=True,
    )

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = _("Forum Kategorisi")
        verbose_name_plural = _("Forum Kategorileri")

    
class ForumSubCategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, verbose_name=_("Kategori"))
    subcategory_name = models.CharField(_("Alt Kategori İsmi"), max_length=100)
    subcategory_explanation = models.CharField(_("Açıklama"), blank=False)
    visible = models.BooleanField(_("Görünür mü?"), default=True)

    def __str__(self):
        return self.subcategory_name
    
    class Meta:
        verbose_name = _("Forum Alt Kategorisi")
        verbose_name_plural = _("Forum Alt Kategorileri")

class ForumThread(models.Model):
    thread_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(_("Başlık"), blank=False)
    body = RichTextField(_("İçerik"), blank=False)
    category = models.ForeignKey(ForumCategory, blank=False, on_delete=models.CASCADE, verbose_name=_("Kategori"))
    subcategory = models.ForeignKey(ForumSubCategory, blank=False, on_delete=models.CASCADE, verbose_name=_("Alt Kategori"))
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, verbose_name=_('Kullanıcı'))
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"),auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Konu Başlığı")
        verbose_name_plural = _("Konu Başlıkları")

class ForumComment(models.Model):
    comment_id = models.AutoField(primary_key=True, unique=True)
    thread_id = models.ForeignKey(ForumThread, null=True, on_delete=models.CASCADE, verbose_name=_("Forum Gönderi ID'si"))
    body = RichTextField(_("İçerik"), blank=False)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, verbose_name=_('Kullanıcı'))
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    reported = models.BooleanField(_("Şikayet"), default=False)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)

    def __str__(self):
        return self.body
    
    class Meta:
        verbose_name = _("Konu Yorumu")
        verbose_name_plural = _("Konu Yorumları")

class ForumLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    liked_comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, null=True, blank=True)
    liked_thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Forum Beğenisi")
        verbose_name_plural = _("Forum Beğenileri")


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(_("E-posta Adresi"),blank=False)
    name_surname = models.CharField(_("İsim-Soyisim"), blank=False)
    title = models.CharField(_("Başlık"), blank=False)
    body = RichTextField(_("İçerik"), blank=False)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title   
    class Meta:
        verbose_name = _("İletişim Formu")
        verbose_name_plural = _("İletişim Formu")
