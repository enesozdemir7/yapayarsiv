from django.shortcuts import render,redirect,get_object_or_404
from course.models import FAQ,SiteSettings,Notifications
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def generalSettingsView(request):
    if request.user.is_superuser:
        obj = SiteSettings.objects.all().last()

        if 'saveButton' in request.POST:

            get_site_title= request.POST.get('title',None)
            get_site_desc= request.POST.get('desc',None)
            get_site_keywords= request.POST.get('keywords',None)
            get_site_fav_icon= request.FILES.get('fav_icon',None)
            get_site_logo = request.FILES.get('logo',None)
            get_site_dark_logo = request.FILES.get('dark_logo',None)

            if get_site_title and get_site_keywords and get_site_desc:

                if obj:
                    obj.title = get_site_title
                    obj.desc = get_site_desc
                    obj.keywords = get_site_keywords
                    
                    if get_site_fav_icon:
                        obj.fav_icon = get_site_fav_icon
                    if get_site_logo:
                        obj.logo = get_site_logo
                    if get_site_dark_logo:
                        obj.dark_logo = get_site_dark_logo

                    obj.save()

                else:
                    obj = SiteSettings.objects.create(title=get_site_title,desc=get_site_desc,keywords=get_site_keywords,
                                                fav_icon=get_site_fav_icon,logo=get_site_logo,dark_logo=get_site_dark_logo)
                
                messages.success(request,"Genel Ayarlar başarıyla kaydedildi.")
                return redirect('management:general-settings')
        
        context = {
            'title':'Genel Ayarlar',
            'obj':obj,
        }
        return render(request,'course/management/settings/general-settings.html',context)



