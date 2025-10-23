from django.shortcuts import render
from course.models import UserPayments
from django.db.models import Sum
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from users.models import CustomUser
from course.models import Course

def indexView(request):
    if request.user.is_superuser:
        get_payments = UserPayments.objects.filter(~Q(status=None))

        get_total_course = Course.objects.filter(active=True).count()
        get_total_members = CustomUser.objects.filter(course_user=True).count()
        total_amount = get_payments.filter(status=True).aggregate(total_amount=Sum('amount'))['total_amount']
        if total_amount is None:
            total_amount = 0
        return render(request,'course/management/index.html',{'total_course':get_total_course,
                                                              'total_members':get_total_members,
                                                              'total_amount':total_amount,
                                                              })




def paymentsView(request):
    if request.user.is_superuser:
        
        get_payments = UserPayments.objects.filter(~Q(status=None))
        current_date = timezone.now()
        seven_days_ago = current_date - timezone.timedelta(days=7)
        one_mounth_ago = current_date - timezone.timedelta(days=7)

        total_amount = get_payments.filter(status=True).aggregate(total_amount=Sum('amount'))['total_amount']
        total_count = get_payments.filter(status=True).count()
        if total_amount is None:
            total_amount = 0
        total_amount_7_days = get_payments.filter(date__gte=seven_days_ago,status=True).aggregate(total_amount=Sum('amount'))['total_amount']
        total_count_7_days = get_payments.filter(date__gte=seven_days_ago,status=True).count()
        if total_amount_7_days is None:
            total_amount_7_days = 0
        total_amount_one_mounth = get_payments.filter(date__gte=one_mounth_ago,status=True).aggregate(total_amount=Sum('amount'))['total_amount']
        total_count_one_mounth = get_payments.filter(date__gte=one_mounth_ago,status=True).count()
        if total_amount_one_mounth is None:
            total_amount_one_mounth = 0
        
        get_q = request.GET.get('q',None)
        if get_q:
            get_payments = get_payments.filter(Q(merchant_oid__icontains=get_q) |Q(user__username__icontains=get_q))



        paginated_number = 20
        blog_count = get_payments.count()
        get_page = request.GET.get('page',1)

        if get_payments:

            paginator = Paginator(get_payments,paginated_number)
            get_payments = paginator.get_page(get_page)
        
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
            
        showing_title = f"{blog_count} Ödemeden {start}-{end} arası gösteriliyor."
        context = {
            'title':'Ödemeler',
            'payments':get_payments,
            'blog_count':blog_count,
            'showing_title':showing_title,
            'q':get_q,
            'total_amount':total_amount,
            'total_count':total_count,
            'total_amount_7_days':total_amount_7_days,
            'total_count_7_days':total_count_7_days,
            'total_amount_one_mounth':total_amount_one_mounth,
            'total_count_one_mounth':total_count_one_mounth,
        }

        return render(request,'course/management/payments.html',context)




def membersViews(request):
    if request.user.is_superuser:
        get_members = CustomUser.objects.filter(course_user=True)

        get_q = request.GET.get('q',None)

        if get_q:
            get_members = get_members.filter(Q(username__icontains=get_q) | Q(email__icontains=get_q))

        paginated_number = 20
        blog_count = get_members.count()
        get_page = request.GET.get('page',1)

        if get_members:

            paginator = Paginator(get_members,paginated_number)
            get_members = paginator.get_page(get_page)
        
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
            
        showing_title = f"{blog_count} Üyeden {start}-{end} arası gösteriliyor."
        context = {
            'title':'Üyeler',
            'members':get_members,
            'members_count':blog_count,
            'showing_title':showing_title,
            'q':get_q,
        }
        return render(request,'course/management/members.html',context)
        