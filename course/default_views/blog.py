from django.shortcuts import render,get_object_or_404
from django.shortcuts import render
from course.models import Category
from course.permissions import course_custom_permission
from course.forms import QuillFieldForm

@course_custom_permission('course')
def blogListView(request):

    get_post_id = request.GET.get('post_id',None)
    get_cats = Category.objects.filter(ai_category=False)
    get_ai_cats = Category.objects.filter(ai_category=True)
    get_q = request.GET.get('q',None)
    content_form = QuillFieldForm()
    context = {
        'title':'Hızlı Öğren',
        'get_cats':get_cats,
        'get_ai_cats':get_ai_cats,
        'post_id':get_post_id,
        'form':content_form,
        'q':get_q,
    }
    return render(request,'course/blog/blog-list.html',context)

@course_custom_permission('course')
def catView(request,slug):

    get_cats = Category.objects.filter(ai_category=False)
    get_ai_cats = Category.objects.filter(ai_category=True)
    getCat = get_object_or_404(Category,slug=slug)
  
    context = {
        'title':getCat.name,
        'get_cats':get_cats,
        'get_ai_cats':get_ai_cats,
        'slug':getCat.slug,
    }
    return render(request,'course/blog/category-blog.html',context)

