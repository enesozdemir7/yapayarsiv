from django.shortcuts import render,redirect,get_object_or_404
from course.models import Category,HomeSlider
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def homeSliderView(request):
    if request.user.is_superuser:
        if 'addSlider' in request.POST:
            title = request.POST.get('title',None)
            desc = request.POST.get('desc',None)
            link = request.POST.get('link',None)
            banner = request.FILES.get("aksfileupload[]",None)
            if banner and title and desc:
                HomeSlider.objects.create(title=title,desc=desc,button_link=link,banner=banner,)
                messages.success(request,"Slider başarıyla eklendi.")

                return redirect('management:home-slider')
        slider_list = HomeSlider.objects.all()
        context = {
            'title':'Ana Sayfa Slider',
            'slider_list':slider_list,
        }
        return render(request,'course/management/slider/slider.html',context)

def editSliderView(request,id):
    if request.user.is_superuser:
        get_slider = get_object_or_404(HomeSlider,id=id)

        if 'editSlider' in request.POST:
            title = request.POST.get('title',None)
            desc = request.POST.get('desc',None)
            link = request.POST.get('link',None)
            banner = request.FILES.get("aksfileupload[]",None)

            if banner:
                get_slider.banner = banner
            get_slider.title = title
            get_slider.desc = desc
            get_slider.link = link
            
            get_slider.save()
            messages.success(request,"Slider başarıyla düzenlendi.")
            return redirect('management:home-slider')

            
        context = {
            'title':"Slider Düzenle",
            'get_slider':get_slider,
        }
        return render(request,'course/management/slider/edit-slider.html',context)
    

def deleteSliderView(request,id):
    if request.user.is_superuser:
        get_slider = get_object_or_404(HomeSlider,id=id)

        if 'deleteSlider' in request.POST:
            get_slider.delete()
            messages.success(request,"Slider silindi.")
            return redirect('management:home-slider')

        context = {
            'title':"Slider Sil",
            'get_slider':get_slider,
        }
        return render(request,'course/management/slider/delete-slider.html',context)



def  ajaxSaveCategoryOrderView(request):
    if request.method == 'POST' and request.user.is_superuser:
        sira_listesi =  json.loads(request.body)['sira']
        for q in sira_listesi:
            get_cat = Category.objects.filter(id=q['id']).last()
            
            if get_cat:
                get_cat.index = int(q['index'])
                get_cat.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})