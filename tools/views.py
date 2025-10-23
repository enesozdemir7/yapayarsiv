from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.contrib import messages
from .forms import *
from .models import *
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
from django.db.models import Q



def tool_ajax_loadmore(request):
    get_page = request.POST.get('page',None)
    get_feeList = json.loads(request.POST.get('get_feeList',[]))
    get_subCatList = json.loads(request.POST.get('get_subCatList',[]))
    category = request.POST.get('category',None)
    keyword = request.POST.get('keyword',None)

    if get_page:
        get_page = int(get_page) + 1


        if get_subCatList:
            get_tools = Tool.objects.filter(subcategory__slug__in=get_subCatList)
        else:
            if category:
                get_tools = Tool.objects.filter(subcategory__category__slug__in=[category]).order_by('-created_at').distinct()
            else:
                get_tools = Tool.objects.all().order_by('-created_at')

        if keyword:
            get_tools = get_tools.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | Q(title__icontains=keyword)).distinct()
            

        if get_feeList:
            get_tools = get_tools.filter(fee__in=get_feeList).distinct()
        
        html_design = []
        get_tools = get_tools[(get_page-1)*tools_paging_number:(get_page)*tools_paging_number]
        
        for x in get_tools:
            sub_cats = []
            tool_stars_avg= ToolStars.objects.filter(tool=x).aggregate(Avg('star'))['star__avg']
            for y in x.subcategory.all():
                sub_cats.append({'name':y.name,'slug':y.slug})
            see_more = ''
            if len(strip_tags(x.body)) > 100:
                see_more = '...'
            html_design.append({'tool_name':x.tool_name,
                                'banner_url':x.banner.url,
                                'body':strip_tags(x.body)[:100] + see_more,
                                'star':tool_stars_avg,
                                'link':x.get_absolute_url(),
                                'extra_url':x.get_edit_url(),
                                'cats':sub_cats,
                                'fee':x.fee,
                                })

        if get_tools is None:
            html_design = None
        context = {
            'data':html_design,
            'status':1,
            'page':int(get_page),
            'listing_value':tools_paging_number,
        }
    else:

        context = {
            'data':[],
            'status':-1,
            'page':get_page,
        }

    return JsonResponse(context)



def more_tools(request):
    tool_obj = Tool.objects.all().order_by('-created_at')
    tool_obj = sorted(tool_obj, key=lambda x: not x.sponsored)
    tool_obj = sorted(tool_obj, key=lambda x: not x.is_priority)
    tools = []

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

    return more_items(request, tools, template='more.html', steps=20)

from django.db.models import Q


def index(request):

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
        'more_posts_url': reverse('more'),
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
    return render(request, "index.html", data)


def index_category(request, category):
    
    tools = []
    get_subCatList = []
    get_feeList = []
    go_filter = False

    if request.method == 'POST' and 'btnFilter' in request.POST:
        get_feeList = request.POST.getlist('feeList',[])
        get_subCatList = request.POST.getlist('subCatList',[])
        go_filter = True

    get_cat = get_object_or_404(ToolCategories2,slug=category)
    get_sub_cats = ToolSubCategories.objects.filter(category=get_cat).distinct()
    filter_cat_names = []

    tool_obj = Tool.objects.filter(subcategory__slug__in=list(get_sub_cats.values_list("slug",flat=True))).order_by('-created_at').distinct()
    
    get_tag = request.GET.get('tag',None)
    get_fee = request.GET.get('fee',None)

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
    

    get_all_cats = ToolCategories2.objects.all()
    keyword = request.POST.get("keyword",None)
    if keyword:
        tool_obj = tool_obj.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | Q(title__icontains=keyword)).distinct()
    
    
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

    root_url = get_cat.get_absolute_url()

    data = {
        'more_posts_url': reverse('more'),
        'keyword':keyword,
        'get_all_cats':get_all_cats,
        'category':category,
        'get_cat':get_cat,
        'tools_count':tools_count,
        "get_sub_cats":get_sub_cats,
        "get_subCatList":get_subCatList,
        "get_feeList":get_feeList,
        "go_filter":go_filter,
        "get_tag":get_tag,
        'root_url':root_url,
        'filter_cat_names':filter_cat_names,
        "title":"Türkiye'nin Yapay Zeka Arşivi; Binlerce Yapay Zeka Aracı İçin Tek Platform!",
        "load_more":load_more,
    }

    data.update(paginated)
    return render(request, "index.html", data)



def index_sub_category(request, category,sub_category):
    
    tools = []

    get_cat = get_object_or_404(ToolSubCategories,sub_category__category__slug=category,sub_category__slug=sub_category)
    tool_obj = Tool.objects.filter(category__slug=category,sub_category___slug__in=[sub_category]).order_by('-created_at')
    get_all_cats = ToolCategories2.objects.all()

    keyword = request.POST.get("keyword")
    if keyword:
        tool_obj = tool_obj.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | Q(title__icontains=keyword)).distinct()
        tool_obj = sorted(tool_obj, key=lambda x: not x.sponsored)
        tool_obj = sorted(tool_obj, key=lambda x: not x.is_priority)
        return render(request, "index.html", {"feed":tool_obj,"keyword":keyword,"get_all_cats":get_all_cats,})

    else:
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
                            pagination_steps=18
                            )
    
    data = {
        'more_posts_url': reverse('more'),
        'keyword':keyword,
        'get_all_cats':get_all_cats,
    }

    data.update(paginated)
    return render(request, "index.html", data)


def rate(request, slug, rating):
    tool = get_object_or_404(Tool, slug=slug)
    tool_stars, created = ToolStars.objects.get_or_create(user=request.user, tool=tool, star=rating)
    messages.success(request,"Başarıyla oy verildi!")
    return redirect("tools:tool",slug=slug)

from django.http import JsonResponse
def get_sub_cats(request,cat_id):
    if request.user.is_authenticated:
        get_sub_cats = ToolSubCategories.objects.filter(category__id=cat_id)
        sub_cats= []
        for x in get_sub_cats:
            sub_cats.append({'id':x.id,'name':x.name})
        return JsonResponse({'sub_cats':sub_cats})

def tool(request, slug):
    tool_obj = get_object_or_404(Tool, slug = slug)
    related_tools = Tool.objects.filter(subcategory__in=tool_obj.subcategory.all()).exclude(slug=tool_obj.slug).order_by("?").distinct()[0:3]
    if request.user.is_authenticated:
        rating = ToolStars.objects.filter(user=request.user, tool = tool_obj).first()
        tool_obj.user_rating = rating.star if rating else 0
    
    all_rating = ToolStars.objects.filter(tool = tool_obj)
    
    
    total_point, one_star, two_star, three_star, four_star, five_star = 0, 0, 0, 0, 0, 0
    for rt in all_rating:
        if rt.star == 1:
            one_star += 1
        elif rt.star == 2:
            two_star += 1
        elif rt.star == 3:
            three_star += 1
        elif rt.star == 4:
            four_star += 1
        elif rt.star == 5:
            five_star += 1
        total_point += rt.star

    star_rating, rating_count = 0, 0 
    if len(all_rating) > 0:
        rating_count = len(all_rating)
        star_rating = round(total_point/rating_count, 1)
        one_star = int((one_star*100) / rating_count )
        two_star = int((two_star*100) / rating_count )
        three_star = int((three_star*100) / rating_count )
        four_star = int((four_star*100) / rating_count )
        five_star = int((five_star*100) / rating_count )

    context = {
        "tool": tool_obj,
        "star_rating": star_rating,
        "rating_count": rating_count,
        "one_star": one_star,
        "two_star": two_star,
        "three_star": three_star,
        "four_star": four_star,
        "five_star": five_star,
        "related_tools":related_tools,
        "title":tool_obj.tool_name
    }

    return render(request, "tool.html", context)

def categories(request):
    return render(request, "categories.html")

@csrf_exempt
@staff_member_required
def manage_tools(request):
    keyword = request.GET.get("keyword")
    if keyword:
        tool_name_results = Tool.objects.filter(tool_name__contains = keyword)
        title_results = Tool.objects.filter(title__contains = keyword)
        body_results = Tool.objects.filter(body__contains = keyword)
        tools = list(chain(tool_name_results, title_results, body_results))
        return render(request, "manage_tools.html", {"tools":tools})

    tools = Tool.objects.order_by('-created_at')[:10]
    context = {
        "tools": tools,
        "title":"Araç Yönetimi",


    }
    return render(request, "manage_tools.html", context)

@csrf_exempt
@staff_member_required
def add_tool(request):
    form = ToolCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        get_sub_cat_list = request.POST.getlist('subcategory',[])

        creating_tool = form.save()
        creating_tool.subcategory.add(*ToolSubCategories.objects.filter(id__in=get_sub_cat_list))
        creating_tool.save()

        messages.success(request,"Araç başarıyla oluşturuldu!")
        return redirect("tools:manage_tools")
        
    return render(request, "add_tool.html", {"form": form,"title":"Araç ekle",})

@csrf_exempt
@staff_member_required
def update_tool(request, slug):
    tool_obj = get_object_or_404(Tool, slug=slug)
    form = ToolChangeForm(request.POST or None, request.FILES or None, instance = tool_obj)
    if form.is_valid():
        get_sub_cat_list = request.POST.getlist('subcategory',[])
        
        tool_form = form.save()
        tool_form.subcategory.add(*ToolSubCategories.objects.filter(id__in=get_sub_cat_list))
        tool_form.save()

        messages.success(request, "Araç başarıyla güncellendi!")
        return redirect("tools:manage_tools")
    return render(request, "update_tool.html", {"form": form,"title":"Araç Güncelle",})

@staff_member_required
def delete_tool(request, slug):
    tool_obj = get_object_or_404(Tool, slug=slug)
    tool_obj.delete()
    messages.success(request, "Araç başarıyla silindi!")
    return redirect("tools:manage_tools")

@login_required
def add_favorited(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    favorited_tool, created = ToolFavoritedUsers.objects.get_or_create(user=request.user, tool=tool)
    messages.success(request, "Araç başarıyla favori listesine alındı!")
    return redirect("index")


@login_required
def remove_favorited(request, fav_id):
    favorited_tool = ToolFavoritedUsers.objects.filter(user=request.user, id=fav_id).last()
    if favorited_tool:
        favorited_tool.delete()
        messages.success(request, "Araç başarıyla kaldırıldı!")
    else:
        messages.info(request, "Araç favori listesinde bulunamadı!")
        
    return redirect("user:favorites")

@staff_member_required
def manage_ads(request):
    tools = Tool.objects.filter(sponsored = True)
    context = {
        "tools": tools
    }
    return render(request, "manage_ads.html", context)


@staff_member_required
def delete_ad(request, id):
    tool_obj = get_object_or_404(Tool, tool_id=id)
    tool_obj.sponsored = False
    tool_obj.save()
    messages.success(request, "Sponsorluk başarıyla kaldırıldı!")
    return redirect("tools:manage_ads")

def category_text(category):
    if category == "Metin":
        return "Text"
    elif category == "Görsel":
        return "Image"
    elif category == "Kodlama":
        return "Code"
    elif category == "Ses":
        return "Sound"
    elif category == "Video":
        return "Video"
    elif category == "3D":
        return "3D"
    elif category == "İşletme":
        return "Business"
    else:
        return "Others"


@staff_member_required
def start_app(request):
    import csv
    import os

    csv_file_path = os.path.join(settings.BASE_DIR, 'tools.csv')

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:

        csv_reader = csv.DictReader(csv_file)
        csv_reader = sorted(csv_reader, key=lambda x: random())

        for row in csv_reader:
            banner = str(row['banner']).replace('/meta_gorsel/','banners/')
            subcategories = row['subcategory'].split(",")
            
            cat_name = str(row['category']).title()
            cat_control = ToolCategories2.objects.filter(name=cat_name).last()
            
            if cat_control is None:
                cat_control = ToolCategories2.objects.create(name=cat_name)
            sub_cat_list = []
            
            for sub_cat in subcategories:
                
                sub_cat = sub_cat.title()
                
                sub_cat_control = ToolSubCategories.objects.filter(name=sub_cat).last()
                
                if sub_cat_control is None:
                    sub_cat_control = ToolSubCategories.objects.create(name=sub_cat)
                sub_cat_control.category.add(*[cat_control])
                sub_cat_list.append(sub_cat_control.id)
            sub_cats = ToolSubCategories.objects.filter(id__in=sub_cat_list)
            
            try:
                tool = Tool.objects.create(
                    tool_name=row['tool_name'],
                    title=row['title'],
                    banner=banner,
                    body=row['body'],
                    #category=cat_control,
                    fee=row['fee'],
                    product_url=row['product_url'],
                    is_priority=row['is_priority'],
                    sponsored=row['sponsored'],
                    visible=row['visible'],
                )
                tool.subcategory.add(*sub_cats)
            except Exception as e:
                pass
    return redirect("index")



