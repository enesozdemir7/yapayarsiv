from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.core.paginator import Paginator
from course.models import BlogComments,HelpComments
from django.contrib import messages

def blogCommentsView(request):
    if request.user.is_superuser:
        get_comments = BlogComments.objects.all()

        get_q = request.GET.get('q',None)

        if get_q:
            get_comments = get_comments.filter(Q(user__username__icontains=get_q) | Q(blog__id__icontains=get_q))

        paginated_number = 20
        comments_count = get_comments.count()
        get_page = request.GET.get('page',1)

        if get_comments:

            paginator = Paginator(get_comments,paginated_number)
            get_comments = paginator.get_page(get_page)
        
        start = 1+ (int(get_page)*paginated_number) - paginated_number
        end =(int(get_page)*paginated_number)

        if comments_count == 0:
            start = 0
            end = 0
        else:

            if end > comments_count:
                end = comments_count
            if start > comments_count:
                start = 1
            
        showing_title = f"{comments_count} Yorumdan {start}-{end} arası gösteriliyor."
        context = {
            'title':'Blog Yorumları',
            'comments':get_comments,
            'comments_count':comments_count,
            'showing_title':showing_title,
            'q':get_q,
        }
        return render(request,'course/management/comments/blog-comments.html',context)
        

def helpCommentsView(request):
    if request.user.is_superuser:
        get_comments = HelpComments.objects.all()

        get_q = request.GET.get('q',None)

        if get_q:
            get_comments = get_comments.filter(Q(user__username__icontains=get_q) | Q(help__id__icontains=get_q))

        paginated_number = 20
        comments_count = get_comments.count()
        get_page = request.GET.get('page',1)

        if get_comments:

            paginator = Paginator(get_comments,paginated_number)
            get_comments = paginator.get_page(get_page)
        
        start = 1+ (int(get_page)*paginated_number) - paginated_number
        end =(int(get_page)*paginated_number)

        if comments_count == 0:
            start = 0
            end = 0
        else:

            if end > comments_count:
                end = comments_count
            if start > comments_count:
                start = 1
            
        showing_title = f"{comments_count} Yardım Postundan {start}-{end} arası gösteriliyor."
        context = {
            'title':'Yardım Yorumları',
            'comments':get_comments,
            'comments_count':comments_count,
            'showing_title':showing_title,
            'q':get_q,
        }
        return render(request,'course/management/comments/help-comments.html',context)
        


def deleteBlogCommentView(request,id):
    if request.user.is_superuser:
        get_comment = get_object_or_404(BlogComments,id=id)

        if 'deleteComment' in request.POST:
            get_comment.delete()
            messages.success(request,"Yorum silindi.")
            return redirect('management:blog-comments')


        context = {
            'title':"Blog Yorumu Sil",
            'get_comment':get_comment,
        }
        return render(request,'course/management/comments/delete-blog-comment.html',context)
    


def deleteHelpCommentView(request,id):
    if request.user.is_superuser:
        get_comment = get_object_or_404(HelpComments,id=id)

        if 'deleteComment' in request.POST:
            get_comment.delete()
            messages.success(request,"Yorum silindi.")
            return redirect('management:help-comments')


        context = {
            'title':"Yardım Yorumu Sil",
            'get_comment':get_comment,
        }
        return render(request,'course/management/comments/delete-help-comment.html',context)