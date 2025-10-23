from django.shortcuts import render
from course.permissions import course_custom_permission

@course_custom_permission('course')
def helpListView(request):
    post_id = request.GET.get('post_id', None)
    query = request.GET.get('q', None)
    
    context = {
        'title': 'Yardım Al',
        'post_id': post_id,
        'query': query,
    }
    return render(request, 'course/help/help-list.html', context)
