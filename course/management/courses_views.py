from django.shortcuts import render,redirect,get_object_or_404
from course.models import Course,CourseSection,CourseSectionLesson,CompletedCourses
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.http import JsonResponse

def courseView(request):
    if request.user.is_superuser:
        if 'addCourse' in request.POST:
            get_title = request.POST.get('title',None)
            get_desc = request.POST.get('desc',None)

            get_banner = request.FILES.get("aksfileupload[]",None)
            if get_title and get_desc and get_banner:

                Course.objects.create(active=False,title=get_title,banner=get_banner,desc=get_desc)
                messages.info(request,"Kurs başarıyla oluşturuldu.")
                return redirect('management:course')
            else:
                messages.info(request,"Kurs oluşturmak için gerekli tüm alanlar doldurulmalıdır.")
                return redirect('management:course')      
        get_courses = Course.objects.all()

        get_q = request.GET.get('q',None)

        if get_q:
            get_courses = get_courses.filter(Q(title__icontains=get_q))

        paginated_number = 20
        course_count = get_courses.count()
        get_page = request.GET.get('page',1)
        if get_courses:

            paginator = Paginator(get_courses,paginated_number)
            get_courses = paginator.get_page(get_page)
        
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
        
            
        showing_title = f"{course_count} Kurstan {start}-{end} arası gösteriliyor."
        context = {
            'title':'Blog',
            'courses':get_courses,
            'course_count':course_count,
            'showing_title':showing_title,
            'q':get_q,
        }
        return render(request,'course/management/courses/courses.html',context)



def manageCourseView(request,id):
    if request.user.is_superuser:
        get_course = get_object_or_404(Course,id=id)
        get_course_sections = CourseSection.objects.filter(course=get_course)
        if 'addSection' in request.POST:
            get_name = request.POST.get('name',None)
            if get_name:
                CourseSection.objects.create(name=get_name,course=get_course)
                messages.info(request,"Bölüm başarıyla eklendi.")
                return redirect('management:manage-course',id=id)

        context = {
            'title':get_course.title,
            'get_course':get_course,
            'get_course_sections':get_course_sections,
        }
        return render(request,'course/management/courses/manage-course.html',context)

def manageSectionView(request,id):
    if request.user.is_superuser:
        get_course_section = get_object_or_404(CourseSection,id=id)
        get_course_lessons = CourseSectionLesson.objects.filter(course_section=get_course_section)


        context = {
            'title':get_course_section.name,
            'get_course_section':get_course_section,
            'get_course_lessons':get_course_lessons,
        }
        return render(request,'course/management/courses/manage-course-section.html',context)

def addLessonView(request,id):
    if request.user.is_superuser:
        get_course_section = get_object_or_404(CourseSection,id=id)

        if request.method == 'POST':
            get_title = request.POST.get('title',None)
            get_vimeo_embed_link = request.POST.get('vimeo_embed_link',None)
            get_video_time = request.POST.get('video_time',None)
            get_content = request.POST.get('content',None)

            if get_title and (get_vimeo_embed_link or get_content):
                
                CourseSectionLesson.objects.create(course_section=get_course_section,title=get_title,vimeo_embed_link=get_vimeo_embed_link,video_time=get_video_time,content=get_content)

                messages.success(request,"Ders başarıyla eklendi.")
                return redirect('management:manage-section',id=id)

        context = {
            'title':'Ders Ekle',
            'get_course_section':get_course_section,
        }
        return render(request,'course/management/courses/add-lesson.html',context)

def editCourseView(request,id):
    if request.user.is_superuser:
        get_course = get_object_or_404(Course,id=id)

        if 'editCourse' in request.POST:
            get_title = request.POST.get('title',None)
            get_desc = request.POST.get('desc',None)
            get_active = request.POST.get('active',None)
            get_banner = request.FILES.get("aksfileupload[]",None)

            get_course.title = get_title
            get_course.desc = get_desc
            if get_active:
                get_course.active = True
            else:
                get_course.active = False
                
            if get_banner:
                get_course.banner = get_banner
            get_course.save()
            messages.success(request,"Kurs başarıyla düzenlendi.")

            return redirect('management:course')

            
        context = {
            'title':"Kurs Düzenle",
            'get_course':get_course,
        }
        return render(request,'course/management/courses/edit-course.html',context)

def editSectionView(request,id):
    if request.user.is_superuser:
        get_section = get_object_or_404(CourseSection,id=id)

        if 'editSection' in request.POST:
            get_name = request.POST.get('name',None)
            if get_name:

                get_section.name = get_name
                get_section.save()
                messages.success(request,"Bölüm başarıyla düzenlendi.")
                return redirect('management:manage-course',id=get_section.course.id)

            else:
                messages.success(request,"Boş alan bırakılmamalıdır.")
            
        context = {
            'title':"Bölüm Düzenle",
            'get_section':get_section,
        }
        return render(request,'course/management/courses/edit-section.html',context)

def editLessonView(request,id):
    if request.user.is_superuser:
        get_lesson = get_object_or_404(CourseSectionLesson,id=id)

        if request.method == 'POST':
            get_title = request.POST.get('title',None)
            get_vimeo_embed_link = request.POST.get('vimeo_embed_link',None)
            get_content = request.POST.get('content',None)
            get_video_time = request.POST.get('video_time',None)
          
            if get_title and (get_vimeo_embed_link or get_content):
                
                get_lesson.title = get_title
                get_lesson.vimeo_embed_link = get_vimeo_embed_link
                get_lesson.content = get_content
                get_lesson.video_time = get_video_time
                get_lesson.save()
                
                messages.success(request,"Ders başarıyla düzenlendi.")
                return redirect('management:manage-section',id=get_lesson.course_section.id)

        context = {
            'title':'Ders Düzenle',
            'get_lesson':get_lesson,
        }
        return render(request,'course/management/courses/edit-lesson.html',context)

def deleteLessonView(request,id):
    if request.user.is_superuser:
        get_lesson = get_object_or_404(CourseSectionLesson,id=id)

        if 'deleteLesson' in request.POST:

            get_lesson.delete()
            messages.success(request,"Ders başarıyla silindi.")
            return redirect('management:manage-section',id=get_lesson.course_section.id)


            
        context = {
            'title':"Dersi Sil",
            'get_lesson':get_lesson,
        }
        return render(request,'course/management/courses/delete-lesson.html',context)

def deleteCourseView(request,id):
    if request.user.is_superuser:
        get_course = get_object_or_404(Course,id=id)

        if 'deleteCourse' in request.POST:

            get_course.delete()
            messages.success(request,"Kurs başarıyla silindi.")
            return redirect('management:course')

            
        context = {
            'title':"Kurs Sil",
            'get_course':get_course,
        }
        return render(request,'course/management/courses/delete-course.html',context)

def deleteSectionView(request,id):
    if request.user.is_superuser:
        get_section = get_object_or_404(CourseSection,id=id)

        if 'deleteSection' in request.POST:

            get_section.delete()
            messages.success(request,"Bölüm başarıyla silindi.")
            return redirect('management:manage-course',id=get_section.course.id)
            
        context = {
            'title':"Bölüm Sil",
            'get_section':get_section,
        }
        return render(request,'course/management/courses/delete-section.html',context)

def ajaxSaveSectionLessonOrderView(request):
    if request.method == 'POST' and request.user.is_superuser:
        sira_listesi =  json.loads(request.body)['sira']
        for q in sira_listesi:
            get_cat = CourseSectionLesson.objects.filter(id=q['id']).last()
            
            if get_cat:
                get_cat.index = int(q['index'])
                get_cat.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def ajaxSaveCourseSectionOrderView(request):
    if request.method == 'POST' and request.user.is_superuser:
        sira_listesi =  json.loads(request.body)['sira']
        for q in sira_listesi:
            get_cat = CourseSection.objects.filter(id=q['id']).last()
            
            if get_cat:
                get_cat.index = int(q['index'])
                get_cat.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def memberCourseProgress(request):
    if request.user.is_superuser:
        all_courses = Course.objects.filter(active=True)

        paginated_number = 20
        course_count = all_courses.count()
        get_page = request.GET.get('page',1)
        if all_courses:

            paginator = Paginator(all_courses,paginated_number)
            all_courses = paginator.get_page(get_page)
        
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

        showing_title = f"{course_count} Kurstan {start}-{end} arası gösteriliyor."

        context = {
            'title':'Kurs İlerlemeleri',
            'courses':all_courses,
            'showing_title':showing_title,
        }
        
        return render(request,'course/management/courses/member_course_progress.html',context)

from users.models import CustomUser

def memberCourseProgressDetail(request,id):

    if request.user.is_superuser:
        get_course = get_object_or_404(Course,id=id)
        all_progress_list = list(CompletedCourses.objects.filter(lesson__course_section__course=get_course).distinct("user").values_list('user__user_id',flat=True))
        all_progress = CustomUser.objects.filter(user_id__in=all_progress_list)

        get_q = request.GET.get('q',None)

        if get_q:
            all_progress = all_progress.filter(Q(username__icontains=get_q))

        paginated_number = 20
        course_count = all_progress.count()
        get_page = request.GET.get('page',1)
        if all_progress:

            paginator = Paginator(all_progress,paginated_number)
            all_progress = paginator.get_page(get_page)
        
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

        showing_title = f"{course_count} İlerlemeden {start}-{end} arası gösteriliyor."

        context = {
            'title':f'{get_course.title} İlerlemeleri',
            'all_progress':all_progress,
            'showing_title':showing_title,
            'course_count':course_count,
            'get_id':id,
            'q':get_q,
        }
        
        return render(request,'course/management/courses/member_course_progress_detail.html',context)