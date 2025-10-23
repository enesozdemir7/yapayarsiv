from django.shortcuts import render,get_object_or_404
from course.models import FAQ,Category,NotificationsUsers
from django.shortcuts import render
from django.db.models import Q
##
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils.safestring import mark_safe
from infscroll.views import more_items
from infscroll.utils import get_pagination
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from itertools import chain
import math
from random import random
from yapayarsiv.settings import tools_paging_number
from django.db.models import Avg
import json
from tools.forms import *
from tools.models import *
from django.core.paginator import Paginator
from course.permissions import course_custom_permission

@course_custom_permission('course')
def sssView(request):
    q = request.GET.get('q',None)
    if q:
        obj = FAQ.objects.filter(Q(question__icontains=q) | Q(reply__icontains=q))
    else:
        obj = FAQ.objects.all()

    context = {
        'title':'Sıkça Sorulan Sorular',
        'obj':obj,
        'q':q,
    }
    return render(request,'course/basic_pages/faq.html',context)

@course_custom_permission('course')
def notificationsView(request):
    
    all_obj = NotificationsUsers.objects.filter(user=request.user)


    get_q = request.GET.get('q',None)

    if get_q:
        all_obj = all_obj.filter(Q(notification__title__icontains=get_q) |Q(notification__link__icontains=get_q))


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
        'title':'Bildirimler',
        'all_obj':all_obj,
        'q':get_q,
        'showing_title':showing_title,

    }
    return render(request,'course/default/notifications.html',context)

@course_custom_permission('course')
def categoryView(request):

    obj = Category.objects.filter(ai_category=False)

    context = {
        'title':'Kategoriler',
        'obj':obj,
    }
    return render(request,'course/basic_pages/category.html',context)
@course_custom_permission('course')
def promptsView(request):


    context = {
        'title':'Promptlar',
    }
    return render(request,'course/basic_pages/prompts.html',context)

@course_custom_permission('course')
def aiCategoryView(request):
    
    obj = Category.objects.filter(ai_category=True)

    context = {
        'title':'AI Araç Kategorileri',
        'obj':obj,
    }
    return render(request,'course/basic_pages/ai-tool-category.html',context)

@course_custom_permission('course')
def toolsView(request):
    
    get_all_cats = ToolCategories2.objects.all()

    tools = []

    get_feeList = []
    get_subCatList = []

    go_filter = False

    if request.method == 'POST' and 'btnFilter' in request.POST:
        get_feeList = request.POST.getlist('feeList',[])
        get_subCatList = request.POST.getlist('subCatList',[])
        go_filter = True

    keyword = request.POST.get("keyword",None)
    if keyword:
        tool_obj = Tool.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | Q(title__icontains=keyword)).distinct()
    else:
        tool_obj = Tool.objects.all().order_by('-created_at')


    get_tag = request.GET.get('tag',None)
    get_fee = request.GET.get('fee',None)

    filter_cat_names = []

    if get_tag:
        get_subCatList = [get_tag]
        filter_cat = ToolSubCategories.objects.filter(slug=get_tag).last()
        if filter_cat:
            filter_cat_names = [filter_cat.name]
            
        tool_obj = tool_obj.filter(subcategory__slug__in=get_subCatList).distinct()
    if get_fee:
        get_feeList = [get_fee]
        tool_obj = tool_obj.filter(fee__in=get_feeList).distinct()


    if go_filter:
        if get_subCatList:
            filter_cat_names = list(ToolSubCategories.objects.filter(slug__in=get_subCatList).values_list('name',flat=True))
            tool_obj = tool_obj.filter(subcategory__slug__in=get_subCatList).distinct()

        if get_feeList:
            tool_obj = tool_obj.filter(fee__in=get_feeList).distinct()


    get_sub_cats = ToolSubCategories.objects.all()
    
    tools_count = tool_obj.count()

    
    tool_obj = sorted(tool_obj, key=lambda x: not x.sponsored)
    tool_obj = sorted(tool_obj, key=lambda x: not x.is_priority)

    tool_star_dict = {}
    tool_stars_obj = ToolStars.objects.all()
    for tool_stars in tool_stars_obj:
        tool_name = tool_stars.tool.tool_name
        if tool_name in tool_star_dict.keys():
            tool_star_dict[tool_name] = {
                'vote_point': tool_star_dict[tool_name]['vote_point'] + tool_stars.star,
                'vote_count': tool_star_dict[tool_name]['vote_count'] + 1,
            }
        else:
            tool_star_dict[tool_name] = {'vote_point': tool_stars.star, 'vote_count': 1}
    
    for obj in tool_obj:

        obj.body = strip_tags(obj.body)
        if len(obj.body) > 100:
            obj.body = obj.body[:100] + " ..."

        if obj.tool_name in tool_star_dict.keys():
            obj.star = math.ceil(
                tool_star_dict[obj.tool_name]['vote_point'] / tool_star_dict[obj.tool_name]['vote_count']
            )
        else:
            obj.star = 0
        
        tools.append(obj)

    paginated = get_pagination(request, tools, 
                            page_canonical=request.GET.get('page', None),
                            shuf=request.GET.get('shuffle', False),
                            pagination_steps=tools_paging_number
                            )

    load_more = True
    if len(paginated['feed']) < tools_paging_number:
        load_more = False

    root_url = '/'
    data = {
        'more_posts_url': '',
        'keyword':keyword,
        'get_all_cats':get_all_cats,
        'tools_count':tools_count,
        'go_filter':go_filter,
        'get_feeList':get_feeList,
        'get_subCatList':get_subCatList,
        'get_tag':get_tag,
        'root_url':root_url,
        'filter_cat_names':filter_cat_names,
        'get_sub_cats':get_sub_cats,
        "title":"Türkiye'nin Yapay Zeka Arşivi; Binlerce Yapay Zeka Aracı İçin Tek Platform!",
        'load_more':load_more,
        
    }

    data.update(paginated)
    return render(request, "course/basic_pages/tools.html", data)
