from django.shortcuts import render,get_object_or_404,redirect
from course.models import Help,Blog,Category
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def helpView(request):
    if request.user.is_superuser:

        get_blogs = Help.objects.all()

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
            'title':'Yardım Paylaşımları',
            'blogs':get_blogs,
            'blog_count':blog_count,
            'showing_title':showing_title,
            'q':get_q,
        }

        return render(request,'course/management/help.html',context)




def editHelpView(request,id):
    if request.user.is_superuser:
        get_help = get_object_or_404(Help,id=id)

        if 'editHelp' in request.POST:
            
            get_title = request.POST.get('title',None)
            get_details = request.POST.get('details',None)
          
            if get_title and get_details:

                
                get_help.title = get_title
                get_help.details = get_details
                
                get_help.save()


                messages.success(request,"Yardım Paylaşımı başarıyla düzenlendi.")
                return redirect('management:help')

        context = {
            'title':'Yardım Paylaşımı Düzenle',
            'get_help':get_help,
        }
        return render(request,'course/management/edit-help.html',context)



def deleteHelpView(request,id):
    if request.user.is_superuser:
        get_blog = get_object_or_404(Help,id=id)

        if 'deleteBlog' in request.POST:
            get_blog.delete()
            messages.success(request,"Yardım Paylaşımı silindi.")
            return redirect('management:help')


        context = {
            'title':"Yardım Paylaşımı Sil",
            'get_blog':get_blog,
        }
        return render(request,'course/management/delete-help.html',context)