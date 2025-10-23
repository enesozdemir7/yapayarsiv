from django.shortcuts import render,get_object_or_404,redirect
from course.models import Help,Blog,Category,UserPayments
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from course.permissions import course_custom_permission
from datetime import datetime, timedelta
from django.utils.timezone import localtime
import pytz

@course_custom_permission('course')
def userBlogView(request):

    get_blogs = Blog.objects.filter(author=request.user)

    get_q = request.GET.get('q',None)

    if get_q:
        get_blogs = get_blogs.filter(Q(title__icontains=get_q) | Q(content__icontains=get_q))

    paginated_number = 20
    blog_count = get_blogs.count()
    get_page = request.GET.get('page',1)

    if get_blogs:

        paginator = Paginator(get_blogs,paginated_number)
        get_blogs = paginator.get_page(get_page)
    
    start = 1+ (int(get_page)*paginated_number) - paginated_number
    end =(int(get_page)*paginated_number)
    if blog_count == 0:
        start = 0
        end = 0
    else:

        if end > blog_count:
            end = blog_count
        if start > blog_count:
            start = 1
        
    showing_title = f"{blog_count} Paylaşımdan {start}-{end} arası gösteriliyor."
    context = {
        'title':'Paylaşımlarım',
        'blogs':get_blogs,
        'blog_count':blog_count,
        'showing_title':showing_title,
        'q':get_q,
    }

    return render(request,'course/user/blog.html',context)



@course_custom_permission('course')
def editUserBlogView(request,id):
    get_cats = Category.objects.filter(ai_category=False)
    get_ai_cats = Category.objects.filter(ai_category=True)
    get_blog = get_object_or_404(Blog,id=id,author=request.user)
    if request.method == 'POST':
        
        get_cat_list = request.POST.getlist('cats',[])
        get_title = request.POST.get('title',None)
        get_content = request.POST.get('content',None)
        video_embed_link = request.POST.get('video_embed_link',None)
        get_banner = request.FILES.get("aksfileupload[]",None)
        
        if get_cat_list and get_title and get_content:

            get_selected_cats = Category.objects.filter(id__in=get_cat_list)
            
            get_blog.title = get_title
            get_blog.video_embed_link = video_embed_link
            get_blog.content = get_content
            if get_banner:
                get_blog.banner = get_banner
            
            get_blog.save()

            get_blog.category.set(get_selected_cats)

            messages.success(request,"Paylaşım başarıyla düzenlendi.")
            return redirect('user:blog')

    context = {
        'title':'Paylaşım Düzenle',
        'get_cats':get_cats,
        'get_ai_cats':get_ai_cats,
        'get_blog':get_blog,
    }
    return render(request,'course/user/edit-blog.html',context)


@course_custom_permission('course')
def deleteUserBlogView(request,id):
    get_blog = get_object_or_404(Blog,id=id,author=request.user)

    if 'deleteBlog' in request.POST:
        get_blog.delete()
        messages.success(request,"Paylaşım silindi.")
        return redirect('user:blog')


    context = {
        'title':"Paylaşım Sil",
        'get_blog':get_blog,
    }
    return render(request,'course/user/delete-blog.html',context)


@course_custom_permission('course')
def userHelpView(request):
    
    get_blogs = Help.objects.filter(user=request.user)

    get_q = request.GET.get('q',None)

    if get_q:
        get_blogs = get_blogs.filter(Q(title__icontains=get_q) |Q(details__icontains=get_q))

    paginated_number = 20
    blog_count = get_blogs.count()
    get_page = request.GET.get('page',1)

    if get_blogs:

        paginator = Paginator(get_blogs,paginated_number)
        get_blogs = paginator.get_page(get_page)
    
    start = 1+ (int(get_page)*paginated_number) - paginated_number
    end =(int(get_page)*paginated_number)
    if blog_count == 0:
        start = 0
        end = 0
    else:

        if end > blog_count:
            end = blog_count
        if start > blog_count:
            start = 1
        
    showing_title = f"{blog_count} Paylaşımdan {start}-{end} arası gösteriliyor."
    context = {
        'title':'Yardım Paylaşımlarım',
        'blogs':get_blogs,
        'blog_count':blog_count,
        'showing_title':showing_title,
        'q':get_q,
    }

    return render(request,'course/user/help.html',context)



@course_custom_permission('course')
def editUserHelpView(request,id):
    get_help = get_object_or_404(Help,id=id,user=request.user)

    if 'editHelp' in request.POST:
        
        get_title = request.POST.get('title',None)
        get_details = request.POST.get('details',None)
        
        if get_title and get_details:

            
            get_help.title = get_title
            get_help.details = get_details
            
            get_help.save()


            messages.success(request,"Yardım Paylaşımı başarıyla düzenlendi.")
            return redirect('user:help')

    context = {
        'title':'Yardım Paylaşımı Düzenle',
        'get_help':get_help,
    }
    return render(request,'course/user/edit-help.html',context)


@course_custom_permission('course')
def deleteUserHelpView(request,id):
    get_blog = get_object_or_404(Help,id=id,user=request.user)

    if 'deleteBlog' in request.POST:
        get_blog.delete()
        messages.success(request,"Yardım Paylaşımı silindi.")
        return redirect('user:help')


    context = {
        'title':"Yardım Paylaşımı Sil",
        'get_blog':get_blog,
    }
    return render(request,'course/user/delete-help.html',context)




@course_custom_permission('course')
def userPaymentsView(request):
    
    get_payments = UserPayments.objects.filter(user=request.user)
    get_payments = get_payments.filter(~Q(status=None))

    get_q = request.GET.get('q',None)

    if get_q:
        get_payments = get_payments.filter(Q(merchant_oid__icontains=get_q))



    paginated_number = 20
    blog_count = get_payments.count()
    get_page = request.GET.get('page',1)

    if get_payments:

        paginator = Paginator(get_payments,paginated_number)
        get_payments = paginator.get_page(get_page)
    
    start = 1+ (int(get_page)*paginated_number) - paginated_number
    end =(int(get_page)*paginated_number)
    if blog_count == 0:
        start = 0
        end = 0
    else:

        if end > blog_count:
            end = blog_count
        if start > blog_count:
            start = 1
        
    showing_title = f"{blog_count} Ödemeden {start}-{end} arası gösteriliyor."
    end_permission = 0
    if request.user.course_joined:
        local_tz = pytz.timezone('Europe/Istanbul')
        start_date = request.user.course_joined.astimezone(local_tz)
        future_date = start_date + timedelta(days=365)
        current_date = datetime.now(local_tz)
        difference = future_date - current_date
        end_permission = difference.days
    context = {
        'title':'Ödemelerim',
        'payments':get_payments,
        'blog_count':blog_count,
        'showing_title':showing_title,
        'q':get_q,
        'end_permission':end_permission,
    }

    return render(request,'course/user/payments.html',context)