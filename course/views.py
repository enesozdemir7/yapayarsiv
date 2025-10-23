from django.shortcuts import render,redirect
import hmac,base64,hashlib,json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yapayarsiv.settings import http_protocol,course_domain,paytr_debug_on,paytr_test_mode,course_site_price
from .models import UserPayments
import requests
import time,uuid
from yapayarsiv.settings import join_images_path
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from users.forms import LoginForm,RegisterForm
from users.models import CustomUser
from course.permissions import course_custom_permission
from yapayarsiv.settings import paytr_merchant_id,paytr_merchant_key,paytr_merchant_salt
from .models import Blog,Help,FAQ,Course,HomeSlider
from django.db.models import Q
from yapayarsiv.settings import site_domain
from django.utils import timezone

@course_custom_permission('course')
def indexView(request):
    get_last_courses = Course.objects.filter(active=True)[0:4]
    get_sliders = HomeSlider.objects.all()
    return render(request,'course/index.html',{'title':'Ana Sayfa','courses':get_last_courses,'sliders':get_sliders,})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

import os

def list_image_names(directory):
    image_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_names.append("payment_page_images/"+filename)
    return image_names

# Klasör yolu

from course.models import CouponCode,UserCoupon
def joinview(request):
    user_c = None
    if request.user.is_authenticated:
        if request.user.course_user:
            return redirect('index')
        
        user_c = UserCoupon.objects.filter(user=request.user,used=False).last()
        if user_c:
            if user_c.coupon.limit < 1:
                user_c.delete()
                user_c = None

    image_names = list_image_names(join_images_path)

    
    if 'paymentPayTR' in request.POST:
        
        c_code = None
        if user_c:
            if user_c.coupon.discount_amount:
                course_site_price_new = course_site_price - user_c.coupon.discount_amount
                c_code = user_c.coupon
            elif user_c.coupon.discount_percent:
                course_site_price_new = course_site_price - (course_site_price * user_c.coupon.discount_percent/100)
                c_code = user_c.coupon
                
        else:
            course_site_price_new = course_site_price

        get_deposit_balance = course_site_price_new
        
        get_payment_country = request.POST.get('payment_country',None)
        get_payment_address = request.POST.get('payment_address',None)
        get_payment_zip_code = request.POST.get('payment_zip_code',None)
        if get_deposit_balance and get_payment_address and get_payment_country and get_payment_zip_code:



            merchant_id = paytr_merchant_id
            merchant_key = paytr_merchant_key.encode(encoding="Utf-8")
            merchant_salt = paytr_merchant_salt.encode(encoding="Utf-8")


            payment_amount = str(int(round(float(get_deposit_balance),2)*100))

            merchant_oid = f"U{request.user.user_id}" + "O" +  str(int(time.time())) 
            user_name = request.user.username
            user_address = get_payment_address
            user_phone = '00000000000000'

            merchant_ok_url = "{}://{}/odeme-basarili/".format(http_protocol,course_domain)
            merchant_fail_url = '{}://{}/odeme-hatasi/'.format(http_protocol,course_domain)

            user_basket = base64.b64encode(json.dumps([["Yapay Arşiv Kurs", str(get_deposit_balance) + " TL", 1],]).encode())

            user_ip = "88.241.109.108"

            timeout_limit = '30'
            debug_on = paytr_debug_on
            test_mode = paytr_test_mode
            no_installment = '0' 
            max_installment = '0'


            hash_str = str(merchant_id + user_ip + merchant_oid + request.user.email + payment_amount + user_basket.decode() + no_installment + max_installment + 'TL' + test_mode)
            paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

            params = {
                'merchant_id': merchant_id,
                'user_ip': user_ip,
                'merchant_oid': merchant_oid,
                'email': request.user.email,
                'payment_amount': payment_amount,
                'paytr_token': paytr_token,
                'user_basket': user_basket,
                'debug_on': debug_on,
                'no_installment': no_installment,
                'max_installment': max_installment,
                'user_name': user_name,
                'user_address': user_address,
                'user_phone': user_phone,
                'merchant_ok_url': merchant_ok_url,
                'merchant_fail_url': merchant_fail_url,
                'timeout_limit': timeout_limit,
                'currency': 'TL',
                'test_mode': test_mode,
            }

            cur_url = "https://www.paytr.com/odeme/api/get-token"
            response = requests.post(cur_url, data=params, )
            ress = response.json()
            if ress['status'] == 'success':
                UserPayments.objects.create(user=request.user,merchant_oid=merchant_oid,amount=get_deposit_balance,coupon_code=c_code)
                return render(request,'course/paytr-page.html',{'ress':ress,})

            elif ress['status'] == 'failed':
                pass
    elif 'couponCodeButton' in request.POST:
        coupon_code = request.POST.get('coupon_code',None)
        get_coupon_code = CouponCode.objects.filter(code=coupon_code,limit__gte=1).last()

        if get_coupon_code:
            user_c = UserCoupon.objects.filter(coupon=get_coupon_code,user=request.user).last()
            if user_c is None:
                if UserCoupon.objects.filter(user=request.user,used=False):
                    messages.info(request,'Zaten uygulanmış bir kuponunuz var.')
                    return redirect('join')              
                user_c = UserCoupon.objects.create(coupon=get_coupon_code,user=request.user)
                messages.info(request,'Kupon kodu uygulandı.')
                return redirect('join')
            else:
                if user_c:
                    if user_c.used:
                        messages.info(request,'Bu kupon kodu zaten kullanılmış.')
                        return redirect('join')
        else:
            messages.info(request,'Kupon bulunamadı.')
            return redirect('join')

    elif 'removeCouponCodeButton' in request.POST:
        UserCoupon.objects.filter(user=request.user,used=False).delete()
        return redirect('join')


    if user_c:
        if user_c.coupon.discount_amount:
            course_site_price_new = course_site_price - user_c.coupon.discount_amount
        elif user_c.coupon.discount_percent:
            course_site_price_new = course_site_price - (course_site_price * user_c.coupon.discount_percent/100)
        else:
            course_site_price_new = course_site_price
    else:
        course_site_price_new = course_site_price

    context = {
        'title':'Hemen Katıl',
        'course_site_price':course_site_price,
        'course_site_price_new':course_site_price_new,
        'image_names':image_names,
        'user_c':user_c,
    }
    return render(request,'course/join.html',context)


@csrf_exempt
def paytrCallback(request):

    merchant_key = paytr_merchant_key.encode(encoding="Utf-8")
    merchant_salt = paytr_merchant_salt

    post = request.POST

    
    try:

        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    except Exception as e:
        pass
    if str(hash.decode()) == post['hash']:

        if request.POST['status'] == 'success':
            
            payment_data = UserPayments.objects.filter(merchant_oid=post['merchant_oid']).first()

            user_c = UserCoupon.objects.filter(user=payment_data.user,used=False,coupon__code=payment_data.coupon_code).last()
            if user_c:
                user_c.coupon.limit -= 1
                user_c.used = True
                user_c.coupon.save()
                user_c.save()


            payment_data.status = True
            payment_data.checked = False
            payment_data.user.course_user = True
            payment_data.user.course_joined = timezone.now()
            payment_data.user.save()
            payment_data.save()

            return HttpResponse((str('OK')))

        else:
            payment_data = UserPayments.objects.filter(merchant_oid=post['merchant_oid']).first()
            payment_data.status = False
            payment_data.checked = False
            payment_data.save()

            return HttpResponse((str('OK')))

    else:
        return HttpResponse((str('OK')))
    

def loginView(request):
    if request.user.is_authenticated == False:

        form = LoginForm(request.POST or None)
        context = {
            "form": form,
            "title":"Giriş Yap",
        }
        if request.method == "POST":
            if form.is_valid():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")

                user = authenticate(email=email, password=password)
                if user is None:
                    messages.info(request, "E-Posta veya parola yanlıştır.")
                else:
                    if True:
                        login(request, user)
                        return redirect("index")
                    else:
                        user.mail_token = uuid.uuid4()
                        user.save()
                        
                        try:
                            send_mail_after_registration(user.email,user.mail_token)
                        except:
                            pass

                        messages.warning(request, "Lütfen e-posta adresinizi doğrulayınız.")

        return render(request,'course/login.html',context)
    else:
        return redirect('index')

@course_custom_permission('course')
def logoutView(request):
    logout(request)
    return redirect("login")

def deliveryandreturnView(request):
    return render(request,'course/delivery-and-return.html',{'title':'Teslimat Ve İade Politikası'})

def privacypolicyView(request):
    return render(request,'course/privacy-policy.html',{'title':'Yapay Arşiv Akademi - Gizlilik Politikası'})

def paymentErrorView(request):
    if request.user.is_authenticated == False:
        return redirect('join')
    return render(request,'course/payment-error.html',{'title':'Ödeme Hatası'})

def paymentSuccessView(request):
    return render(request,'course/payment-successful.html',{'title':'Ödeme Başarılı'})


def registerView(request):
    if request.user.is_authenticated == False:

        form = RegisterForm(request.POST or None)
        get_next = request.GET.get('next',None)
        context = {
            "form": form,
            "title":"Kayıt Ol",
            'get_next':get_next,
        }

        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                
                new_user = CustomUser(
                    username=username,
                    email = email,
                    name = "",
                    surname = "",
                    mail_token = str(uuid.uuid4())
                    )
                new_user.set_password(password)
                new_user.save()
                try:
                    send_mail_after_registration(new_user.email,new_user.mail_token)
                except:
                    pass
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Kayıt olma işlemi tamamlanmıştır. Hoşgeldiniz!")
                if get_next:
                    return redirect(get_next)
                return redirect('index')
                #return redirect("index")
        return render(request,'course/register.html',context)
    else:
        return redirect('index')

from django.core.mail import EmailMultiAlternatives
from yapayarsiv.settings import EMAIL_HOST_USER

def sendMail(subject,content,email):
    msg = EmailMultiAlternatives(subject,content,EMAIL_HOST_USER, email)
    msg.attach_alternative(content, "text/html")
    msg.send(fail_silently=False)
    

def send_mail_after_registration(email,token):
    subject = "Yapay Arşiv Hesabınızın doğrulanması gerekiyor"
    message = f'Merhaba Yapay Arşiv hesabınızı doğrulamak için bağlantıya tıklayın; <a href="https://{site_domain}/email-onay/onay/{token}">Tıklayınız</a>'
    recipient_list = [email]
    sendMail(subject, message , recipient_list)