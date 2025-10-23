from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from users.models import CustomUser
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from infscroll.views import more_items
from infscroll.utils import get_pagination
from django.urls import reverse
from itertools import chain
from django.db.models import Q
from django.core.paginator import Paginator
from yapayarsiv.settings import posts_paging_number
from django.http import JsonResponse

def post_ajax_loadmore(request):

    get_page = request.POST.get('page',None)
    keyword = request.POST.get('keyword',None)
    if get_page:
        get_page = int(get_page) + 1

        if keyword:
            posts = Post.objects.filter(no=keyword,visible=True).distinct().order_by('-created_at')
        else:
            posts = Post.objects.filter(visible=True).order_by('-created_at')

        posts = posts[(get_page-1)*posts_paging_number:(get_page)*posts_paging_number]   
        html_design = []   
        for x in posts:
    
            html_design.append({'no':x.no,
                                'image_url':x.thumbnail.url,
                                'url':x.url,
                                })
        if posts is None:
            html_design = None

        context = {
            'data':html_design,
            'status':1,
            'page':int(get_page),
            'listing_value':posts_paging_number,
        }

    else:
        context = {
            'data':[],
            'status':-1,
            'page':get_page,
        }

    return JsonResponse(context)

from django.shortcuts import render

def post(request, id):
    post = get_object_or_404(Post, post_id=id)
    return render(request, "post.html", {"post":post,"title":post.title})

def news(request, slug):
    news = get_object_or_404(News, slug=slug)
    get_other_news = News.objects.all().exclude(news_id=news.news_id)[0:3]
    return render(request, "news.html", {"news": news,"get_other_news":get_other_news,"title":news.title})

def more_posts(request):

    posts = Post.objects.order_by('-created_at')
    return more_items(request,posts, template="more_posts.html")
    
def all_post(request):


    keyword = request.POST.get("keyword",None)
    if keyword:
        posts = Post.objects.filter(no=keyword,visible=True).distinct().order_by('-created_at')
    else:

        posts = Post.objects.filter(visible=True).order_by('-created_at')

    paginated = get_pagination(request, posts, 
                            page_canonical=request.GET.get('page', None),
                            shuf=request.GET.get('shuffle', False),
                            pagination_steps=posts_paging_number
                            )
    load_more = True
    if len(paginated['feed']) < posts_paging_number:
        load_more = False
    data = {
        'more_posts_url': reverse('more'),
        'keyword':keyword,
        "title":"Gönderiler",
        'load_more':load_more,
    }
    data.update(paginated)
    return render(request, "all_posts.html", data)
    

def all_news(request):

    news_obj = News.objects.filter(visible=True)

    paginator = Paginator(news_obj,12)
    page = request.GET.get('sayfa')
    news_obj = paginator.get_page(page)

    context = {
        "news":news_obj,
        "title":"Haberler",
    }
    return render(request, "all_news.html", context)

@csrf_exempt
def manage_news(request):
    keyword = request.GET.get("keyword")

    if keyword:
        # Filter news based on keyword (unchanged)
        title_results = News.objects.filter(title__contains=keyword)
        body_results = News.objects.filter(body__contains=keyword)
        all_news = list(chain(title_results, body_results))

        # Sort results by creation date in descending order (newest first)
        all_news.sort(key=lambda news: news.created_at, reverse=True)

        return render(request, "manage_news.html", {"all_news": all_news})

    else:
        # Fetch top 10 news in descending order of creation date (newest first)
        all_news = News.objects.order_by("-created_at")[:25]

        context = {
            "all_news": all_news,
            "title": "Haberleri Yönet",
        }
        return render(request, "manage_news.html", context)


@csrf_exempt
def manage_posts(request):

    keyword = request.GET.get("keyword")
    if keyword:
        title_results = Post.objects.filter(title__contains = keyword)
        body_results = Post.objects.filter(no__contains = keyword)
        posts = list(chain(title_results, body_results))
        return render(request, "manage_posts.html", {"posts": posts})

    posts = Post.objects.order_by('-created_at')[:10]
    context = {
        "posts": posts,
        "title":"Gönderileri Yönet",

    }
    return render(request, "manage_posts.html", context)

def about(request):
    return render(request, "about.html", {"title":"Hakkımızda"})

def privacy(request):
    return render(request, "privacy.html", {"title":"Gizlilik Politikası ve Sorumluluk Reddi"})

def terms(request):
    return render(request, "terms.html", {"title":"Kullanım Koşulları"})

def error_404_view(request, exception):
    
    return render(request, '404.html', {"title":"404"})
def error_500_view(request, exception):
    
    return render(request, '500.html', {"title":"500"})
def contact(request):

    form = ContactCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Form başarıyla gönderildi!")
        return redirect("forum:contact")
    
    context = {
        "form": form,
        "title":"İletişim",

    }
    return render(request, "contact.html", context)

@staff_member_required
def contact_data(request, id):
    contact_data = get_object_or_404(Contact, contact_id=id)
    return render(request, "contact_data.html", {"contact_data": contact_data})

def forum(request):
    category = ForumCategory.objects.all()
    category_list = []

    for obj in category:
        subcat_list = []
        subcategory = ForumSubCategory.objects.filter(category=obj)
        if len(subcategory) != 0:
            for subcat_obj in subcategory:
                subcat_list.append(
                    {
                        "subcategory_id": subcat_obj.subcategory_id,
                        "subcategory_name": str(subcat_obj)
                    }
                )
        filtered_thread = ForumThread.objects.filter(category=obj)
        thread_count = filtered_thread.count()
        comment_count_list = filtered_thread.annotate(comment_count=models.Count('forumcomment'))
        total_comment_count = sum(comment.comment_count for comment in comment_count_list)
        category_list.append(
            {
                "category_name":str(obj),
                "category_id": obj.category_id,
                "explanation": obj.explanation,
                "subcategories":subcat_list,
                "thread_count": thread_count,
                "comment_count": total_comment_count
            }
        )

    user_obj = CustomUser.objects.all()
    user_count = user_obj.count()

    tool_obj = Tool.objects.all()
    tool_count = tool_obj.count()

    thread_obj = ForumThread.objects.all()
    thread_count = thread_obj.count()

    last_threads = ForumThread.objects.order_by('-created_at')[:15]

    context = {
        "category_list": category_list,
        "user_count": user_count,
        "tool_count": tool_count,
        "thread_count": thread_count,
        "last_threads": last_threads,
        "title":"Forum",

    }
    return render(request, "forum.html", context)

def category(request, id):
    category = ForumCategory.objects.filter(category_id=id).first()

    subcategories = ForumSubCategory.objects.filter(category=category)
    if len(subcategories) == 0:
        pass
    context = {
        "subcategories": subcategories,
        "category_id": str(id),
    }
    return render(request, "forum_category.html", context)

def subcategory(request, category_id, subcategory_id):
    subcategory = ForumSubCategory.objects.filter(subcategory_id=subcategory_id).first()
    threads = ForumThread.objects.filter(subcategory=subcategory)
    context = {
        "threads": threads,
        "category_id":  category_id,
        "subcategory_id": subcategory_id,
    }
    return render(request, "forum_subcategory.html", context)

@csrf_exempt
@staff_member_required
def thread(request, category_id, subcategory_id, thread_id):
    threads = ForumThread.objects.filter(subcategory_id=subcategory_id).first()
    comments = ForumComment.objects.filter(thread_id=thread_id)

    form = ForumCommentCreationForm(request.POST or None)

    if form.is_valid():
        comment_form = form.save(commit=False)
        comment_form.save()
        
        messages.success(request, "Yorum başarıyla gönderildi!")
        return HttpResponseRedirect("forum:forum_thread",category_id=category_id,subcategory_id=subcategory_id,thread_id=thread_id)

    context = {
        "threads": threads,
        "category_id":  category_id,
        "subcategory_id": subcategory_id,
        "comments": comments,
        "form": form,
    }
    return render(request, "forum_thread.html", context)

@csrf_exempt
@staff_member_required
def update_post(request, id):
    post = get_object_or_404(Post, post_id = id)
    form = PostChangeForm(request.POST or None, request.FILES or None, instance = post)
    if form.is_valid():
        post_form = form.save(commit=False)
        post_form.save()
        messages.success(request, "Gönderi başarıyla güncellendi!")
        return redirect("forum:manage_posts")
    return render(request, "update_post.html", {"form": form})

@csrf_exempt
@staff_member_required
def add_post(request):
    form = PostCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post_form = form.save(commit=False)
        post_form.save()
        messages.success(request, "Gönderi başarıyla oluşturuldu!")
        return redirect("forum:manage_posts")
    return render(request, "add_post.html", {"form": form})

@staff_member_required
def delete_post(request, id):
    post_obj = get_object_or_404(Post, post_id=id)
    post_obj.delete()
    messages.success(request, "Gönderi başarıyla silindi!")
    return redirect("forum:manage_posts")

@csrf_exempt
@staff_member_required
def update_news(request, id):
    news = get_object_or_404(News, news_id = id)
    form = NewsChangeForm(request.POST or None, request.FILES or None, instance = news)
    if form.is_valid():
        news_form = form.save(commit=False)
        news_form.save()
        messages.success(request, "Haber başarıyla güncellendi!")
        return redirect("forum:manage_news")
    return render(request, "update_news.html", {"form": form})

@staff_member_required
def add_news(request):
    form = NewsCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        news_form = form.save(commit=False)
        news_form.owner = request.user
        news_form.save()
        messages.success(request, "Haber başarıyla oluşturuldu!")
        return redirect("forum:manage_news")
    return render(request, "add_news.html", {"form": form})

@staff_member_required
def delete_news(request, id):
    news_obj = get_object_or_404(News, news_id=id)
    news_obj.delete()
    messages.success(request, "Haber başarıyla silindi!")
    return redirect("forum:manage_news")
