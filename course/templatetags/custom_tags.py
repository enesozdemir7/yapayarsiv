
from django import template
from course.models import CompletedCourses
from course.models import CourseSectionLesson,CompletedCourses

register = template.Library()


@register.filter
def get_course_progress(user,course_id):

    return int(user.get_course_progress(course_id))