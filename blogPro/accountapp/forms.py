from asyncio.windows_events import NULL
from cProfile import label
import email
from django import forms
from django.contrib.auth.models import User
import re

class loginForm(forms.Form):

    username=forms.CharField(
        label="Kullanıcı Adı",
        max_length=20,
        min_length=10,
        required=True,
        error_messages={
            "max_length":"En fazla 20 karakter girebilirsiniz!",
            "min_length":"En az 10 karakter girmelisiniz!"
        }
    )
    password=forms.CharField(
        label="Şifre",
        max_length=30,
        min_length=10,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'name':'password',
            }
        )  
    )


class authorLoginForm(forms.Form):

    username=forms.CharField(
        label="Kullanıcı Adı",
        max_length=20,
        min_length=10,
        required=True,
        error_messages={
            "max_length":"En fazla 20 karakter girebilirsiniz!",
            "min_length":"En az 10 karakter girmelisiniz!"
        }
    )
    password=forms.CharField(
        label="Şifre",
        max_length=30,
        min_length=10,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'name':'password',
            }
        )  
    )


class registerForm(forms.Form):
    username=forms.CharField(
        label="Kullanıcı Adı",
        max_length=25,
        min_length=10,
        required=True,
    )
    email=forms.EmailField(
        label="E-mail",
        max_length=100,
        min_length=20,
        required=True,
    )
    password=forms.CharField(
        label="Şifre",
        max_length=30,
        min_length=10,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "name":"password",
            }
        )
    )
    re_password=forms.CharField(
        label="Şifre",
        max_length=30,
        min_length=10,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "name":"password",
            }
        )
    )

    # Form class'ın içerisindeki clean metodunu override ettik.
    # Form'dan gelen değerleri clean metodu ile validasyon kontrollerini gerçekleştirdik.

    def clean(self):
        _username=self.cleaned_data.get("username")
        _email=self.cleaned_data.get("email")
        _password=self.cleaned_data.get("password")
        _repassword=self.cleaned_data.get("re_password")

        '''
        if  _username.isdigit(): 
            raise forms.ValidationError("Sadece Alfabetik değer girebilirsiniz!")
        '''
        
        if not re.search("[0-9]",_password and _repassword):
            raise forms.ValidationError("Parolanız'da 0-9 arasında bir adet rakamsal değer olmalı!")

        if not re.search("[A-Z]",_password and _repassword):
            raise forms.ValidationError("Parolanız bir adet büyük harf içermelidir!")

        if not re.search("[a-z]",_password and _repassword):
            raise forms.ValidationError("Parolanız bir adet küçük harf içermelidir!")

        if re.search("\s",_password and _repassword):
            raise forms.ValidationError("Parolanız boşluk karakteri içermemelidir!")

        # gelen veriler boş değilse ve parolalar eşit değilse
        if _password and _repassword is not None and _password!=_repassword: 
            raise forms.ValidationError("Parola'lar eşlemiyor!")

        if User.objects.filter(username=_username).exists():
            raise forms.ValidationError("Bu kullanıcı adı sistemde kayıtlıdır.")

        if User.objects.filter(email=_email).exists():
            raise forms.ValidationError("Bu Mail adresi sistemde kayıtlıdır.")

        # Hata yoksa gelen değerleri views'a gönder
        context={
            "_username":_username,
            "_email":_email,
            "_password":_password,
        }
        return context