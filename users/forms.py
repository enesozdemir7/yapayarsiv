from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from django import forms
import re
def passwordControl(sifre):
    
    if not re.search('[a-zA-Z]', sifre):
        return False
    if not re.search('[0-9]', sifre):
        return False
    return True

class LoginForm(forms.Form):

    email = forms.EmailField(max_length=50, label="E-Posta Adresi",widget=forms.EmailInput)
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=250, label="Kullanıcı Adı",widget=forms.TextInput)
    email = forms.EmailField(max_length=50, label="E-Posta Adresi",widget=forms.EmailInput)
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20, label="Parola Doğrulama", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        if len(password) < 8:
            raise forms.ValidationError("Parolanız en az 8 karakterden oluşmalıdır.")
        if not re.search('[a-zA-Z]', password):
            raise forms.ValidationError("Parolanız rakam ve karakter içermelidir.")
        if len(password) < 8:
            raise forms.ValidationError("Parolanız rakam ve karakter içermelidir.")

        confirm_password = self.cleaned_data.get("confirm_password")

        if not email:
            raise forms.ValidationError("Lütfen geçerli bir e-posta adresi giriniz.")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Parolalar eşleşmiyor.")
            
        try:
            user = CustomUser.objects.get(email=email)
            raise forms.ValidationError("Bu e-posta adresi kullanılmaktadır. Farklı bir e-mail adresi giriniz.")
        except CustomUser.DoesNotExist:
            pass

        try:
            user = CustomUser.objects.get(username=username)
            raise forms.ValidationError("Bu kullanıcı adı kullanılmaktadır. Farklı bir kullanıcı adı giriniz.")
        except CustomUser.DoesNotExist:
            pass

        return {
            'username':username,
            "email": email,
            "password": password
        }
    



class ProfileForm(UserChangeForm):

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['name'].required = False
        self.fields['surname'].required = False
        self.fields['profile_pic'].required = False
        self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields =  ("username","email", "name", "surname", "profile_pic", "biography","website", "github", "instagram",)

    def clean(self):
        username = self.cleaned_data.get("username")
        try:
            user = CustomUser.objects.get(username=username)
            if user:
                if user.username != self.user.username:
                    raise forms.ValidationError("Bu kullanıcı adı kullanılmaktadır. Farklı bir kullanıcı adı giriniz.")
        except CustomUser.DoesNotExist:
            pass


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields =  ("username","email", "name", "surname", "biography", "verified", "editor", "is_staff", "is_active",)


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

    class Meta:
        model = CustomUser
        fields =  ("username","email", "name", "surname", "biography", "verified", "editor", "is_staff", "is_active",)
