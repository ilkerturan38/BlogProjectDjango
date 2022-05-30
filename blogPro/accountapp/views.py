from pickle import FALSE
from django.shortcuts import redirect, render
from .forms import loginForm,registerForm,authorLoginForm
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password



def login(request):
    
    # Eğer kullanıcı sisteme giriş yaptıysa,login sayfasına gitmek istediğinde başka sayfaya yönlendirilsin.
    if request.user.is_authenticated: 
        return redirect("index")
    
    form=loginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data["username"]
        password=form.cleaned_data["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:   
            auth.login(request,user)
            messages.add_message(request,messages.SUCCESS,'Başarılı bir şekilde Giriş Yapıldı..')
            return redirect("blogList")
        else:
            messages.add_message(request,messages.ERROR,'Kullanıcı adı veya Şifre Hatalı!')
    context={
        "form":form,
    }
    return render(request,"account/login.html",context)


# Normal Kullanıcı Kayıt..
def register(request):
    if request.user.is_authenticated: 
        return redirect("index")
    form=registerForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data["_username"]
        email=form.cleaned_data["_email"]
        password = make_password(form.cleaned_data["_password"]) # parolayı veritabanında korumalı parola yapmak için make_password kullanıldı.
        newUser=User(username=username,email=email,password=password)
        #newUser.set_password=password
        newUser.is_superuser=False
        newUser.is_staff=False
        newUser.save()
        messages.add_message(request,messages.SUCCESS,'Kayıt olma işlemi başarılı bir şekilde gerçekleşti..')
        return redirect("index")
    context={
        "form":form
    }
    return render(request,"account/register.html",context)


def logout(request):
    auth.logout(request)
    return redirect("index")



# Bütün kullanıcı bilgileri,tek bir User modeli üzerinden gelmesin,başka model üzerinden de sisteme authenticate,login olmayı deneyim ama olmadı!!!

