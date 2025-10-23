from django.shortcuts import render,redirect,get_object_or_404
from course.models import FAQ
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def faqView(request):
    if request.user.is_superuser:
        if 'addFaq' in request.POST:
            get_question = request.POST.get('question',None)
            get_reply = request.POST.get('reply',None)

            FAQ.objects.create(question=get_question,reply=get_reply)
            messages.success(request,"SSS başarıyla eklendi.")
            return redirect('management:faq')
        
        get_faq_list = FAQ.objects.all()
        context = {
            'title':'Sıkça Sorulan Sorular',
            'get_faq_list':get_faq_list,
        }
        return render(request,'course/management/faq.html',context)


def editFaqView(request,id):
    if request.user.is_superuser:
        get_faq = get_object_or_404(FAQ,id=id)

        if 'saveCategory' in request.POST:

            get_question = request.POST.get('question',None)
            get_reply = request.POST.get('reply',None)

            get_faq.question = get_question
            get_faq.reply = get_reply
            get_faq.save()
            messages.success(request,"SSS başarıyla düzenlendi.")
            return redirect('management:faq')

            
        context = {
            'title':"SSS Düzenle",
            'get_faq':get_faq,
        }
        return render(request,'course/management/edit-faq.html',context)
    

def deleteFaqView(request,id):
    if request.user.is_superuser:
        get_faq = get_object_or_404(FAQ,id=id)

        if 'deleteFaq' in request.POST:
            get_faq.delete()
            messages.success(request,"SSS silindi.")
            return redirect('management:faq')


        context = {
            'title':"SSS Sil",
            'get_faq':get_faq,
        }
        return render(request,'course/management/delete-faq.html',context)
    

def  ajaxSaveFaqOrderView(request):
    if request.method == 'POST' and request.user.is_superuser:
        sira_listesi =  json.loads(request.body)['sira']
        print('sira listesi : ',sira_listesi)
        for q in sira_listesi:
            get_faq = FAQ.objects.filter(id=q['id']).last()
            
            if get_faq:
                get_faq.index = int(q['index'])
                get_faq.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})