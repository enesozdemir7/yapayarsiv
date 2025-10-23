from django.shortcuts import render,redirect,get_object_or_404
from course.models import Category,Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def blogView(request):
    if request.user.is_superuser:
        get_blogs = Blog.objects.all()

        get_q = request.GET.get('q',None)

        if get_q:
            get_blogs = get_blogs.filter(Q(title__icontains=get_q) |Q(desc__icontains=get_q) | Q(content__icontains=get_q))

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
            
        showing_title = f"{blog_count} Blogdan {start}-{end} arası gösteriliyor."
        context = {
            'title':'Blog',
            'blogs':get_blogs,
            'blog_count':blog_count,
            'showing_title':showing_title,
            'q':get_q,
        }
        return render(request,'course/management/blog.html',context)

def addBlogView(request):
    if request.user.is_superuser:
        get_cats = Category.objects.filter(ai_category=False)
        get_ai_cats = Category.objects.filter(ai_category=True)

        if request.method == 'POST':
            get_cat_list = request.POST.getlist('cats',[])
            get_title = request.POST.get('title',None)
            get_content = request.POST.get('content',None)
            video_embed_link = request.POST.get('video_embed_link',None)
            get_banner = request.FILES.get("aksfileupload[]",None)
            
            if get_cat_list and get_title and get_content:
                if get_content != '<p><br></p>':

                    get_selected_cats = Category.objects.filter(id__in=get_cat_list)
                    
                    created_blog = Blog.objects.create(title=get_title,video_embed_link=video_embed_link,content=get_content,author=request.user,banner=get_banner)
                    created_blog.category.add(*get_selected_cats)

                    messages.success(request,"Blog başarıyla eklendi.")
                    return redirect('management:blog')

        context = {
            'title':'Blog Ekle',
            'get_cats':get_cats,
            'get_ai_cats':get_ai_cats,
        }
        return render(request,'course/management/add-blog.html',context)
    

from course.forms import QuillFieldForm
def editBlogView(request,id):
    if request.user.is_superuser:
        get_cats = Category.objects.filter(ai_category=False)
        get_ai_cats = Category.objects.filter(ai_category=True)
        get_blog = get_object_or_404(Blog,id=id)
        content_form = QuillFieldForm()

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

                messages.success(request,"Blog başarıyla düzenlendi.")
                return redirect('management:blog')

        context = {
            'title':'Blog Düzenle',
            'get_cats':get_cats,
            'get_ai_cats':get_ai_cats,
            'get_blog':get_blog,
            'form':content_form,
        }
        return render(request,'course/management/edit-blog.html',context)



def deleteBlogView(request,id):
    if request.user.is_superuser:
        get_blog = get_object_or_404(Blog,id=id)

        if 'deleteBlog' in request.POST:
            get_blog.delete()
            messages.success(request,"Blog silindi.")
            return redirect('management:blog')


        context = {
            'title':"Blog Sil",
            'get_blog':get_blog,
        }
        return render(request,'course/management/delete-blog.html',context)