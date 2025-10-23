from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from forum.models import *
from tools.models import *
from .forms import *
from datetime import date, timedelta
from django.test import override_settings
from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from yapayarsiv.settings import site_domain
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required(login_url= "user:login")
def changePasswordView(request):
    
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user,request.POST or None)

        if 'btnChangePassword' in request.POST:

            if form.is_valid():

                user = form.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Parola Başarıyla Değiştirildi!")
                return redirect('user:profile')

        return render(request,'user/change-password.html',{'title':'Parola Değiştir','form':form,})

def token_send(request):
    return render(request , 'token_send.html')

def success(request):
    return render(request , 'success.html')

@login_required(login_url= "user:login")
def profile(request):
    threads = ForumThread.objects.filter(user=request.user)[:5]
    tool_favorited = ToolFavoritedUsers.objects.filter(user=request.user)[:5]
    profile = get_object_or_404(CustomUser, user_id=request.user.user_id)
    
    thread_found = False
    if len(threads) > 0:
        thread_found = True

    tool_favorited_found = False
    if len(tool_favorited) > 0:
        tool_favorited_found = True

    context = {
        "profile": profile,
        "threads": threads,
        "tool_favorited": tool_favorited,
        "thread_found": thread_found,
        "tool_favorited_found": tool_favorited_found,
        "title":"Profil",
    }
    return render(request, "profile.html", context)

@login_required(login_url= "user:login")
def favorites(request):
    tool_favorited = ToolFavoritedUsers.objects.filter(user=request.user)
        
    return render(request, "favorites.html", {"tool_favorited": tool_favorited,"title":"Favoriler",})


@login_required(login_url= "user:login")
def delete_favorites(request,id):
    tool = Tool.objects.filter(tool_id = id).first()
    tool_favorited = ToolFavoritedUsers.objects.filter(user=request.user, tool=tool).delete()
    return redirect("user:favorites")

@csrf_exempt
@login_required(login_url= "user:login")
def settings(request):
    threads = ForumThread.objects.filter(user=request.user)[:5]
    tool_favorited = ToolFavoritedUsers.objects.filter(user=request.user)[:5]
    form = ProfileForm(request.user,request.POST or None, request.FILES or None, instance = request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Değişiklikler Başarıyla Kaydedildi!")
            return redirect("user:profile")
    
    thread_found = False
    if len(threads) > 0:
        thread_found = True

    tool_favorited_found = False
    if len(tool_favorited) > 0:
        tool_favorited_found = True

    context = {
        "profile": form,
        "threads": threads,
        "tool_favorited": tool_favorited,
        "thread_found": thread_found,
        "tool_favorited_found": tool_favorited_found,
        "title":"Ayarlar",
    }

    return render(request, "settings.html", context)

@staff_member_required
def admin_dashboard(request):

    user_obj = CustomUser.objects.all()
    user_count = user_obj.count()

    with override_settings(USE_TZ=False):
        d = date.today()-timedelta(days=7)
        new_user_obj = CustomUser.objects.filter(date_joined__gte=d)
        new_user_count = new_user_obj.count()

    tool_obj = Tool.objects.all()
    tool_count = tool_obj.count()

    post_obj = Post.objects.all()
    post_count = post_obj.count()

    forum_category_obj = ForumCategory.objects.all()
    forum_category_count = forum_category_obj.count()

    thread_obj = ForumThread.objects.all()
    thread_count = thread_obj.count()

    contact_forms = Contact.objects.order_by('-created_at')[:5]
    reported_comments = ForumComment.objects.filter(reported=True)[:5]

    context = {
        "user_count": user_count,
        "new_user_count": new_user_count,
        "tool_count": tool_count,
        "post_count": post_count,
        "forum_category_count": forum_category_count,
        "thread_count": thread_count,
        "contact_forms": contact_forms,
        "reported_comments": reported_comments,
        "title":"Admin Panel",

    }

    return render(request, "dashboard.html", context)

@csrf_exempt
@staff_member_required
def manage_users(request):
    keyword = request.GET.get("keyword")
    if keyword:
        name_results = CustomUser.objects.filter(name__contains = keyword)
        surname_results = CustomUser.objects.filter(surname__contains = keyword)
        email_results = CustomUser.objects.filter(email__contains = keyword)
        users = list(chain(name_results, surname_results, email_results))
        return render(request, "manage_users.html", {"users":users,"title":"Kullanıcı Yönetimi",})

    users = CustomUser.objects.order_by('-last_login')[:10]
    context = {
        "users": users,
        "title":"Kullanıcı Yönetimi",

    }
    return render(request, "manage_users.html", context)

import uuid
@csrf_exempt
def register(request):
    form = RegisterForm(request.POST or None)
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
            login(request, new_user)
            messages.success(request, "Kayıt olma işlemi tamamlanmıştır. Hoşgeldiniz!")
            return redirect('token_send')
            #return redirect("index")
            
    context = {
        "form": form,
        "title":"Kayıt Ol",
    }
    return render(request, "register.html", context)

def verify(request , mail_token):
    try:
        user_obj = CustomUser.objects.filter(mail_token=mail_token,is_verified=False).first()
        if user_obj:
            user_obj.is_verified = True
            user_obj.save()
            messages.success(request,'Hesabınız onaylandı')
            return redirect('success')
        else:
            return redirect('index')

    except Exception as e:
        pass




@csrf_exempt
def user_login(request):
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
                return render(request, "login.html", context)
            
            if True:
                messages.success(request, "Başarıyla giriş yaptınız.")
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
            
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("index")

@csrf_exempt
@staff_member_required
def update_user(request, id):
    user = get_object_or_404(CustomUser, user_id = id)
    form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance = user)
    if form.is_valid():
        user_form = form.save(commit=False)
        user_form.save()
        messages.success(request, "Kullanıcı hesabı başarıyla güncellendi!")
        return redirect("user:manage_users")
    return render(request, "update_user.html", {"form": form,"title":"Kullanıcı Güncelle",})

@staff_member_required
def block_user(request, id):
    user_obj = get_object_or_404(CustomUser, user_id=id)
    user_obj.blocked = True
    user_obj.save()
    messages.success(request, "Kullanıcı başarıyla yasaklandı!")
    return redirect("user:manage_users")

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