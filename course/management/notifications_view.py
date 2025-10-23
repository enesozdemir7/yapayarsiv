

from django.shortcuts import render,get_object_or_404,redirect
from course.models import Notifications,NotificationsUsers
from django.contrib import messages
from users.models import CustomUser
import threading
from django.core.paginator import Paginator
from django.db.models import Q

def notificationPushThread(title,link,users):
    n = Notifications.objects.create(title=title,link=link,system=True)
    for x in users:
        NotificationsUsers.objects.create(user=x,notification=n)


def notificationsView(request):
    if request.user.is_superuser:
        all_obj = Notifications.objects.filter(system=True)

        if 'addNotification' in request.POST:

            title= request.POST.get('title',None)
            link= request.POST.get('link',None)

            if title:
                get_courser_users = CustomUser.objects.filter(course_user=True)
                threading.Thread(target=notificationPushThread,args=(title,link,get_courser_users)).start()
                messages.success(request,"Bildirimler kullanıcılara gönderiliyor...")
                return redirect('management:notifications')

        get_q = request.GET.get('q',None)

        if get_q:
            all_obj = all_obj.filter(Q(title__icontains=get_q) |Q(link__icontains=get_q))


        paginated_number = 20
        course_count = all_obj.count()
        get_page = request.GET.get('page',1)

        if all_obj:

            paginator = Paginator(all_obj,paginated_number)
            all_obj = paginator.get_page(get_page)
        
        start = 1+ (int(get_page)*paginated_number) - paginated_number
        end =(int(get_page)*paginated_number)
        if course_count == 0:
            start = 0
            end = 0
        else:

            if end > course_count:
                end = course_count
            if start > course_count:
                start = 1

        showing_title = f"{course_count} Bildirimden {start}-{end} arası gösteriliyor."

        context = {
            'title':'Bildirim Yönetimi',
            'all_obj':all_obj,
            'showing_title':showing_title,
            'q':get_q,

        }
        return render(request,'course/management/settings/notification-manager.html',context)
    

def editNotificationsView(request,id):
    if request.user.is_superuser:
        get_course = get_object_or_404(Notifications,id=id)

        if 'editNotification' in request.POST:

            title = request.POST.get('title',None)
            link = request.POST.get('link',None)

            if title:
                get_course.title = title
                get_course.link = link
                get_course.save()
                
                messages.success(request,"Bildirim başarıyla düzenlendi.")
                return redirect('management:notifications')

        context = {
            'title':'Bildirim Yönetimi',
            'get_n':get_course,
        }
        return render(request,'course/management/settings/edit-notification.html',context)


def deleteNotificationsView(request,id):
    if request.user.is_superuser:
        get_n = get_object_or_404(Notifications,id=id)

        if 'deleteNotification' in request.POST:
            get_n.delete()
            messages.success(request,"Bildirim başarıyla silindi.")
            return redirect('management:notifications')

        context = {
            'title':'Bildirim Yönetimi',
            'get_n':get_n,
        }
        return render(request,'course/management/settings/delete-notifications.html',context)
