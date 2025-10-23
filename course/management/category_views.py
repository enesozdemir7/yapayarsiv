from django.shortcuts import render,redirect,get_object_or_404
from course.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def categoryView(request):
    if request.user.is_superuser:
        if 'addCategory' in request.POST:
            get_cat_name = request.POST.get('cat_name',None)
            get_icon = request.FILES.get("aksfileupload[]",None)
            if get_cat_name and get_icon:
                Category.objects.create(ai_category=False,name=get_cat_name,icon=get_icon)
                return redirect('management:category')
        get_category_list = Category.objects.filter(ai_category=False)
        context = {
            'title':'Kategoriler',
            'category_list':get_category_list,
        }
        return render(request,'course/management/category.html',context)

def aiToolCategoryView(request):
    if request.user.is_superuser:
        if 'addCategory' in request.POST:
            get_cat_name = request.POST.get('cat_name',None)
            get_icon = request.FILES.get("aksfileupload[]",None)
            if get_cat_name and get_icon:

                Category.objects.create(ai_category=True,name=get_cat_name,icon=get_icon)
                return redirect('management:ai-tool-category')
        get_category_list = Category.objects.filter(ai_category=True)
        context = {
            'title':'AI Araç Kategorileri',
            'category_list':get_category_list,
        }
        return render(request,'course/management/category.html',context)

def editCategoryView(request,id):
    if request.user.is_superuser:
        get_cat = get_object_or_404(Category,id=id)

        if 'saveCategory' in request.POST:
            get_cat_name = request.POST.get('cat_name',None)
            get_icon = request.FILES.get("aksfileupload[]",None)
            if get_icon:
                get_cat.icon = get_icon
            get_cat.name = get_cat_name
            
            get_cat.save()
            messages.success(request,"Kategori başarıyla düzenlendi.")

            if get_cat.ai_category:
                return redirect('management:ai-tool-category')
            else:
                return redirect('management:category')
        if get_cat.ai_category:
            title = "AI Araç Kategori Düzenle"
        else:
            title = "Kategori Düzenle"
            
        context = {
            'title':title,
            'get_cat':get_cat,
        }
        return render(request,'course/management/edit-category.html',context)
    

def deleteCategoryView(request,id):
    if request.user.is_superuser:
        get_cat = get_object_or_404(Category,id=id)

        if 'deleteCategory' in request.POST:
            get_cat.delete()
            messages.success(request,"Kategori silindi.")
            return redirect('management:category')

        if get_cat.ai_category:
            title = "AI Araç Kategori Sil"
        else:
            title = "Kategori Sil"

        context = {
            'title':title,
            'get_cat':get_cat,
        }
        return render(request,'course/management/delete-category.html',context)



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