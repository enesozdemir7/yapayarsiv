from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from course.models import SiteSettings 
import codecs,json
from yapayarsiv.settings import general_settings_cache_path


def write_json(path,data):
    with codecs.open(path,'w',encoding="utf-8") as f: 
        json.dump(data, f, indent=4,ensure_ascii=False) 

@receiver(post_save, sender=SiteSettings)
def saveSiteSettings(sender, instance, created, **kwargs):
    jsonData = {'title':instance.title,'desc':instance.desc,'keywords':instance.keywords,'fav_icon':instance.fav_icon.url,'logo':instance.logo.url,'dark_logo':instance.dark_logo.url}
    write_json(general_settings_cache_path,jsonData)

@receiver(pre_delete, sender=SiteSettings)
def deleteSiteSettings(sender, instance, **kwargs):
    jsonData = {'title':'','desc':'','keywords':'','fav_icon':'','logo':'','dark_logo':''}

    write_json(general_settings_cache_path,jsonData)