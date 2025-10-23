from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid
from users.models import CustomUser
from django.urls import reverse

def turkish_to_english(text):
    turkish_chars = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 'İ': 'I', 'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'Ö': 'O', 'Ç': 'C'}
    
    for tr, en in turkish_chars.items():
        text = text.replace(tr, en)
    
    return text

class ToolCategories(models.TextChoices):
    TEXT = "metin", _("Metin")
    IMAGE = "gorsel", _("Görsel")
    CODE = "kodlama", _("Kodlama")
    SOUND = "ses", _("Ses")
    VIDEO = "video", _("Video")
    THREE_DIMENSIONAL = "3d", _("3D işleme")
    BUSINESS = "isletme", _("İşletme")
    OTHERS = "digerleri", _("Diğerleri")

class ToolCategories2(models.Model):

    name = models.CharField(verbose_name=_('Kategori Adı'))
    slug = models.SlugField(unique=True,blank=True,null=True,editable=False)
    index = models.IntegerField(default=0,verbose_name=_('Sıra Numarası'))
    category_icon = models.ImageField(upload_to='category_icons',verbose_name=_('Kategori İkon'),blank=True,null=True)
    color = models.CharField(verbose_name="Arka Plan Rengi örn(#f0f0f0)",max_length=20,blank=True,null=True)

    class Meta:
        ordering = ['index']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
            return reverse("index_category", kwargs={"category": self.slug})
    def hover_index(self):
         return self.index + 1
    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.name)
            get_uuid_key = str(uuid.uuid4())[0:4]
            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(ToolCategories2, self).save(*args, **kwargs)

class ToolSubCategories(models.Model):
    #category = models.ForeignKey(ToolCategories2,verbose_name=_("Üst Kategori"),on_delete=models.CASCADE)
    category = models.ManyToManyField(ToolCategories2,blank=True,verbose_name=_("Alt Kategori"))
    name = models.CharField(verbose_name=_("Alt Kategori Adı"),max_length=100)
    slug = models.SlugField(unique=True,blank=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse("index_sub_category", kwargs={"category": self.category.slug,"sub_category":self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.name)

            get_uuid_key = str(uuid.uuid4())[0:4]
            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(ToolSubCategories, self).save(*args, **kwargs)

class ToolFee(models.TextChoices):
    COMPLETELY_FREE = "Ücretsiz", _("Ücretsiz")
    WITH_FREE_VERSION = "Ücretsiz Sürümlü", _("Ücretsiz Sürümlü")
    FREE_TRIAL = "Ücretsiz Deneme", _("Ücretsiz Deneme")
    PAID = "Ücretli", _("Ücretli")
    OTHERS = "Diğerleri", _("Diğerleri")

class Tool(models.Model):
    tool_id = models.AutoField(primary_key=True, unique=True)
    tool_name = models.CharField(_("Araç İsmi"), blank=False, unique=True)
    title = models.CharField(_("Başlık"), blank=False)
    slug = models.SlugField(unique=True,blank=True,null=True)

    banner = models.ImageField(_("Banner"), upload_to=settings.MEDIA_BANNERS_URL)
    body = RichTextField(_("İçerik"), blank=False)
    #category = models.ForeignKey(ToolCategories2,verbose_name=_("Kategori"), on_delete=models.CASCADE)
    subcategory = models.ManyToManyField(ToolSubCategories,blank=True,verbose_name=_("Alt Kategori"))
    fee = models.CharField(
        _("Ücret"),
        choices=ToolFee.choices,
        default=ToolFee.OTHERS,
        )
    product_url = models.CharField(_("Araç URL"), blank=False)
    is_priority = models.BooleanField(_("Öncelikli mi?"), default=False)
    sponsored = models.BooleanField(_("Sponsorlu mu?"), default=False)
    visible = models.BooleanField(_("Görünür mü?"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma zamanı"), auto_now_add=True)

    def __str__(self):
        return self.tool_name
    
    def get_absolute_url(self):
            return reverse("tools:tool", kwargs={"slug": self.slug})

    def get_edit_url(self):
            return reverse("tools:update_tool", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            clear_slug = turkish_to_english(self.tool_name)

            get_uuid_key = str(uuid.uuid4())[0:4]
            self.slug = str(slugify(clear_slug, allow_unicode=True)) + f"-{get_uuid_key}"

        super(Tool, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Araç")
        verbose_name_plural = _("Araçlar")
        ordering = ['-created_at']

class ToolStars(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    star = models.IntegerField(validators =[MaxValueValidator(5), MinValueValidator(1)])

    class Meta:
        verbose_name = _("Araç Puanı")
        verbose_name_plural = _("Araç Puanı")

class ToolFavoritedUsers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Aracı Favoriye Alan Kullanıcılar")
        verbose_name_plural = _("Aracı Favoriye Alan Kullanıcılar")
