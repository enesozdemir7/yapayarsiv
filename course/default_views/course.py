from django.shortcuts import render,get_object_or_404
from course.models import Course,CourseSection,CourseSectionLesson,CompletedCourses
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from course.permissions import course_custom_permission
from django.db.models import Q

@course_custom_permission('course')
def courseListView(request):
    get_q = request.GET.get('q',None)
    context = {
        'title':'Kurslar',
        'q':get_q,
    }
    return render(request,'course/default/courses.html',context)

@course_custom_permission('course')
def coursePromotionView(request,id):
    get_course = get_object_or_404(Course,id=id,active=True)
    
    get_progress_max = CourseSectionLesson.objects.filter(course_section__course__id=get_course.id).count()
    current_progress = CompletedCourses.objects.filter(lesson__course_section__course__id=get_course.id,user=request.user).count()
    completed_lessons = list(CompletedCourses.objects.filter(lesson__course_section__course__id=get_course.id,user=request.user).values_list('lesson__id',flat=True))
    try:

        current_progress = (current_progress / get_progress_max) * 100
    except:
        current_progress = 0
    context = {
        'title':get_course.title,
        'course':get_course,
        'current_progress':int(current_progress),
        'completed_lessons':completed_lessons,
    }
    return render(request,'course/default/course-promotion.html',context)

@course_custom_permission('course')
def courseDetailView(request,id):
    get_course = get_object_or_404(Course,id=id,active=True)

    default_lesson = request.GET.get('default',None)

    get_progress_max = CourseSectionLesson.objects.filter(course_section__course__id=get_course.id).count()
    current_progress = CompletedCourses.objects.filter(lesson__course_section__course__id=get_course.id,user=request.user).count()
    completed_lessons = list(CompletedCourses.objects.filter(lesson__course_section__course__id=get_course.id,user=request.user).values_list('lesson__id',flat=True))

    try:
        current_progress = (current_progress / get_progress_max) * 100
    except:
        current_progress = 0
    
    first_lesson = None
    
    try:
        first_section = get_course.get_first_section()
        if first_section:
            first_lesson = first_section.get_first_lesson()
    except Exception as e:
        pass
    
    context = {
        'title':get_course.title,
        'course':get_course,
        'completed_lessons':completed_lessons,
        'current_progress':int(current_progress),
        'first_lesson':first_lesson,
        'default_lesson':default_lesson,
    }
    return render(request,'course/default/course-detail.html',context)


@api_view(['POST'])
@course_custom_permission('course')
def getLessonDetailView(request):
    if request.user.is_authenticated:
    
        data_key = request.POST.get('data_key',None)
        complete = request.POST.get('complete',None)
        if data_key:
            get_lesson = get_object_or_404(CourseSectionLesson,id=data_key,course_section__course__active=True)
            complete_lesson = None
            current_progress = 0

            if complete:
                get_complete_lesson = get_object_or_404(CourseSectionLesson,id=complete)
                obj, created = CompletedCourses.objects.get_or_create(user=request.user, lesson=get_complete_lesson, defaults={'user': request.user,'lesson':get_complete_lesson})

                complete_lesson = get_complete_lesson.id
                
                get_progress_max = CourseSectionLesson.objects.filter(course_section__course__id=get_complete_lesson.course_section.course.id).count()
                current_progress = CompletedCourses.objects.filter(lesson__course_section__course__id=get_complete_lesson.course_section.course.id,user=request.user).count()
                current_progress = (current_progress / get_progress_max) * 100

            return Response({'status':True,'data':{'title':get_lesson.title,
                                                    'vimeo_embed_link':get_lesson.vimeo_embed_link,
                                                    'content':get_lesson.content,
                                                    'complete_lesson':complete_lesson,
                                                    'progress':int(current_progress),}}, 
                                                    status=status.HTTP_200_OK)
        elif complete:

            get_complete_lesson = get_object_or_404(CourseSectionLesson,id=complete)
            obj, created = CompletedCourses.objects.get_or_create(user=request.user, lesson=get_complete_lesson, defaults={'user': request.user,'lesson':get_complete_lesson})
            
            complete_lesson = get_complete_lesson.id
            
            get_progress_max = CourseSectionLesson.objects.filter(course_section__course__id=get_complete_lesson.course_section.course.id).count()
            current_progress = CompletedCourses.objects.filter(lesson__course_section__course__id=get_complete_lesson.course_section.course.id,user=request.user).count()
            current_progress = (current_progress / get_progress_max) * 100

            return Response({'status':True,'data':{'progress':int(current_progress),
                                                    'complete_lesson':complete_lesson,
                                                   }}, 
                                                    status=status.HTTP_200_OK)
      
        else:
            return Response({'status':False,'data':{}}, status=status.HTTP_404_NOT_FOUND)
            

