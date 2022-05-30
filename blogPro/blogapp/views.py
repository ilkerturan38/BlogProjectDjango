
from asyncio.windows_events import NULL
import email
from hashlib import new
from logging.config import listen
from multiprocessing import context
from re import X
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .models import category,blog,author,aboutt,comment, ortak
from .forms import blogForm,categoryForm,authorForm,aboutForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password,check_password,MD5PasswordHasher
from django.db.models import Q

#-------------------------INDEX------------------------------------

def index(request):
    sorgu=blog.objects.select_related("categories").all() # Foreign Bağlantılı categori içeriklerine ulaşma (Daha Az Veritabanı Sorgusu çalıştırır)
    paginator=Paginator(sorgu,4)
    page = request.GET.get('page',1)
    try:
        icerik = paginator.page(page)
    except PageNotAnInteger :
        icerik = paginator.page(1)
    except EmptyPage:
        icerik = paginator.page(paginator.num_pages)
    
    # Birden fazla aynı CategoryID'deki,blog kayıtlarından son eklenen kaydı getirme işlemi 

    islem1=blog.objects.filter(categories__name="gundem").order_by("-title").first()
    islem2=blog.objects.filter(categories__name="teknoloji").order_by("-title").first()
    islem3=blog.objects.filter(categories__name="saglik").order_by("-title").first()
    islem4=blog.objects.filter(categories__name="yazilim").order_by("-title").first()
    islem5=blog.objects.filter(categories__name="spor").order_by("-title").first()

    '''
    for item in sorgu:
        for items in item.authors.all():
            print(items)
    '''

    context={
        #"blogGetir":blog.objects.filter(status=True) # Foreign Bağlantılı categori içerikleri ulaşma (Daha Çok Veritabanı Sorgusu çalıştırır)
        "blogGetir":icerik,
        "record1":islem1,
        "record2":islem2,
        "record3":islem3,
        "record4":islem4,
        "record5":islem5
    }
    return render(request,'blog/index.html',context)

#-----------------------BLOG-DETAILS-------------------------------

def blogDetails(request,id):
    islem=get_object_or_404(blog,id=id)
    
    #islem2=blog.objects.get(id=id).authors.first() => SideBar Sağ Menü 1
    islem2=blog.objects.prefetch_related('authors').get(id=id).authors.latest("id")
    
    # Yazara göre,Sadece tek bir blog kaydı getirme işlemi
    '''  
    islem3=author.objects.prefetch_related('blogs').get(id=islem2.id).blogs.all()
    for item in islem3:
        islem4=item
    '''
    
    # Yazara göre,Bütün blog kayıtlarını getirme işlemi 
    
    islem3=author.objects.filter(id=islem2.id) # => SideBar Sağ Menü 2
    islem4=NULL
    for item in islem3:
        islem4=item.blogs.all()

    context={
        "blog":islem,
        "comment":islem.comments.all(), # islem'den gelen blogID'ye göre, Yorumları getir. (ters ilişki uygulandı,bloga göre yorumları getir)
        "yazarAdi":islem2.nameSurname,
        "yazarResmi":islem2.imageURL,
        "yazarHakkinda":islem2.about,
        "yazarinBloglari":islem4
    }
    return render(request,"blog/blogDetails.html",context)

#-----------------------CATEGORY-BLOGLİST--------------------------

def categoryBlogList(request,slug):
    #sorgu=blog.objects.filter(categories__slug=slug) # alınan her blog üzerinden,Categori kayıtlarını getirme işlemi.
    try:
        sorgu=category.objects.get(slug=slug).blog_set.all() # alınan her Category üzerinden (Category değerleri her sayfa için tek,ayrı olarak geliyor),Blog kayıtlarını getirme işlemi.
    except sorgu.DoesNotExist: # gelen sorguda,URL'den gelen kategoriye türüne göre hiçbir blog kaydı yoksa sorgu'yu null döndür.
        sorgu=NULL

    paginator=Paginator(sorgu,3)
    page = request.GET.get('page',1)
    try:
        icerik = paginator.page(page)
    except PageNotAnInteger :
        icerik = paginator.page(1)
    except EmptyPage:
        icerik = paginator.page(paginator.num_pages)
    islem=get_object_or_404(category,slug=slug) # URL'de eşleşen category ismine göre, Category tablosundaki ilgili alanlar gösterilir.

    context={
        "category":islem, # blog tablosundaki ilişkili categories değerine göre, __ category modeline git slug değeri al,parametreden gelen ile karşılaştır.
        "blog": icerik,
    }

    return render(request,"blog/categoryBlogList.html",context)

#------------------------CONTACT-----------------------------------

def contact(request):
    return render(request,"blog/contact.html")

#------------------------ABOUT-------------------------------------

def about(request):
    sorgu=aboutt.objects.first()
    sorgu2=author.objects.all()
    sorgu3=author.objects.count()
    context={
        "hakkimizda":sorgu,
        "yazar":sorgu2,
        "toplamyazar":sorgu3
    }
    return render(request,"blog/about.html",context)


#----------------------ADMİN-BLOG----------------------------------


@login_required(login_url="login") 
def blogList(request):
    context={
       
        "blog":blog.objects.all().order_by("title")  # Durumu True olan bloglar,en üste geliyor listelenirken..
    }
    return render(request,"admin/blogList.html",context)


def blogComment(request,id):
    kontrol=get_object_or_404(blog,id=id)
    
    blogs=blog.objects.filter(id=id)
    yorumGetir=NULL
    for item in blogs:
        yorumGetir=item.comments.all() # Ters ilişki yapıldı,related_name değeri alındı.

    context={
        "islem1":kontrol,
        "islem2":yorumGetir
    }
    return render(request,"admin/blogComment.html",context)


def authorBlog(request,id):
    kontrol=get_object_or_404(author,id=id)
    
    yazar=author.objects.filter(id=id)
    blogGetir=NULL
    for item in yazar:
        blogGetir=item.blogs.all().order_by("title")

    context={
        "islem1":kontrol,
        "islem2":blogGetir
    }
    return render(request,"admin/authorBlog.html",context)

def AuthorBlogStatusUpdateFalse(request,id):
    islem=get_object_or_404(blog,id=id)
    islem.status=False
    islem.save()
    # yine tekrardan authorblog sayfası üzerinden yönlendiremedim,Çünkü authorBlog/id(yazarID), bu metotdaki parametre ile gelen id ise blogID eşleşmiyorlar..
    return redirect(reverse('authorList')) 

def AuthorBlogStatusUpdateTrue(request,id):
    islem=get_object_or_404(blog,id=id)
    islem.status=True
    islem.save()
    return redirect(reverse('authorList'))


@login_required(login_url="login") 
def blogInsert(request):
    try:
        form=blogForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            newblog=form.save(commit=False)
            newblog.categories_id=request.POST['categories_id']
            newblog.status=True
            newblog.slug=newblog.title
            newblog.save()
            gelenyazar=request.POST["author_id"]

            d1=blog.objects.get(id=newblog.id)
            d2=author.objects.get(id=gelenyazar)

            d1.authors.add(d2) # Blog üzerinden,Yazar ekleme
            d2.blogs.add(d1) # Yazar üzerinden,Blog Ekleme

            messages.add_message(request,messages.SUCCESS,'Blog ekleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect('index')
            
    except Exception as hata:
            messages.add_message(request,messages.WARNING,'Blog ekleme işlemi sırasında hata meydana geldi!',hata)
    else:
        pass
    context={
        "form":form,
        "category":category.objects.all(),
        "author":author.objects.all()
        }
    return render(request,"admin/blogInsert.html",context)


@login_required(login_url="login") 
def blogUpdate(request,id):
    #sorgu=blog.objects.filter(id=id).first()
    sorgu=get_object_or_404(blog,id=id)
    try:
        form=blogForm(request.POST or None,request.FILES or None,instance=sorgu)
        if form.is_valid():
            islem=form.save(commit=False)
            islem.categories_id=request.POST['categories_id']
            islem.save()
            gelenyazar=request.POST["author_id"]

            d1=blog.objects.get(id=islem.id)
            d2=author.objects.get(id=gelenyazar)
            
            d1.authors.add(d2)
            d2.blogs.add(d1)
             

            messages.add_message(request,messages.SUCCESS,'Blog güncelleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect('blogList')
    except Exception as hata:  
        messages.add_message(request,messages.WARNING,'Blog güncelleme işlemi sırasında hata meydana geldi!',hata) 
    else:
        pass
    context={
        "form":form,
        "value":sorgu,
        "category":category.objects.all(),
        "author":author.objects.all()
        }
    return render(request,"admin/blogUpdate.html",context)

    
def blogDelete(request,id):
    #islem=blog.objects.get(id=id)
    islem=get_object_or_404(blog,id=id)
    try:
        islem.delete()
        messages.add_message(request,messages.SUCCESS,'Blog silme işlemi başarılı bir şekilde gerçekleşti..')
        return redirect('blogList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Blog silme işlemi sırasında hata meydana geldi!',hata)
        return render(request,"admin/blogList.html")


def BlogStatusUpdateFalse(request,id):
    islem=get_object_or_404(blog,id=id)
    islem.status=False
    islem.save()
    return redirect('blogList')

def BlogStatusUpdateTrue(request,id):
    islem=get_object_or_404(blog,id=id)
    islem.status=True
    islem.save()
    return redirect('blogList')

#---------------------ADMİN-BLOG-----------------------------------


#---------------------ADMİN-AUTHOR---------------------------------


@login_required(login_url="login") 
def authorList(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    sorgu=author.objects.all().order_by("nameSurname")
    context={
        "author":sorgu
    }
    return render(request,"admin/authorList.html",context)


# Burdaki kullanıcı adı ve şifre bilgileri alınarak giriş yapılamadı!,User modeli üzerinden yazar(kullanıcı) bilgileri alınarak sisteme authenticate olunuyor..
@login_required(login_url="login") 
def authorInsert(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    try:
        form=authorForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Yazar ekleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect('authorList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Yazar ekleme işlemi sırasında hata meydana geldi!',hata)
    context={
            "form":form
    }
    return render(request,"admin/authorInsert.html",context)


@login_required(login_url="login") 
def authorUpdate(request,id):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    kontrol=get_object_or_404(author,id=id)
    try:
        form=authorForm(request.POST or None,request.FILES or None,instance=kontrol)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Yazar güncelleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect("authorList")      
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Yazar güncelleme işlemi sırasında hata meydana geldi!',hata)
    else:
        pass
    context={
            "form":form,
            "value":kontrol
        }
    return render(request,"admin/authorUpdate.html",context)

def authorDelete(request,id):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    islem=get_object_or_404(author,id=id)
    try:
        islem.delete()
        messages.add_message(request,messages.SUCCESS,'Yazar silme işlemi başarılı bir şekilde gerçekleşti..')
        return redirect('authorList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Yazar silme işlemi sırasında hata meydana geldi!',hata)
        return render(request,"admin/authorList.html")


def authorStatusUpdateTrue(request,id):
    islem=get_object_or_404(author,id=id)
    islem.status=True
    islem.save()
    # manuel olarak URL linki tanımlamak yerine, reverse URL name değerine göre yönlendirme yaparız.
    return redirect(reverse("authorList")) 

def authorStatusUpdateFalse(request,id):
    islem=get_object_or_404(author,id=id)
    islem.status=False
    islem.save()
    return redirect(reverse("authorList"))

#---------------------ADMİN-AUTHOR---------------------------------


#---------------------ADMİN-CATEGORY-------------------------------


@login_required(login_url="login") 
def categoryList(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    sorgu=category.objects.all().order_by("name")
    context={
        "category":sorgu
    }
    return render(request,"admin/categoryList.html",context)


@login_required(login_url="login") 
def categoryInsert(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    try:
        form=categoryForm(request.POST or None)
        if form.is_valid():
            x=form.cleaned_data.get('name')
            newCategory=form.save(commit=False)
            newCategory.name=x
            newCategory.save()
            messages.add_message(request,messages.SUCCESS,'Category ekleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect('categoryList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Category ekleme işlemi sırasında hata meydana geldi!',hata)
    else:
        pass
    context={
        "form":form
        } 
    return render(request,"admin/categoryInsert.html",context)


@login_required(login_url="login") 
def categoryUpdate(request,id):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    kontrol=get_object_or_404(category,id=id)
    try: # Kodlar Denetlenir
        form=categoryForm(request.POST or None,instance=kontrol)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Category güncelleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect("categoryList")      
    except Exception as hata: # Hata Varsa
        messages.add_message(request,messages.WARNING,'Category güncelleme işlemi sırasında hata meydana geldi!',hata)
    else: # Sayfa her açıldığında Kodlar Denetlenir,Hata Yoksa Çalışıcak kısım
        pass
    context={
            "form":form,
            "value":kontrol
        }
    return render(request,"admin/categoryUpdate.html",context)


def categoryDelete(request,id):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    islem=get_object_or_404(category,id=id)
    try:
        islem.delete()
        messages.add_message(request,messages.SUCCESS,'Category silme işlemi başarılı bir şekilde gerçekleşti..')
        return redirect('categoryList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Category silme işlemi sırasında hata meydana geldi!',hata)
        return render(request,"admin/categoryList.html")


def categoryStatusUpdateFalse(request,id):
    islem=get_object_or_404(category,id=id)
    islem.status=False
    islem.save()
    return redirect('categoryList')
    

def categoryStatusUpdateTrue(request,id):
    islem=get_object_or_404(category,id=id)
    islem.status=True
    islem.save()
    return redirect('categoryList')

#---------------------ADMİN-CATEGORY-------------------------------


#---------------------ADMİN--ABOUT---------------------------------


def aboutInsert(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    try:
        form=aboutForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Hakkımızda Bilgisi ekleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect('aboutList')
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Hakkımızda Bilgisi ekleme işlemi sırasında hata meydana geldi!',hata)
    else:
        pass
    context={
        "form":form
    }
    return render(request,"admin/aboutInsert.html",context)

@login_required(login_url="login")
def aboutList(request):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    context={
        "hakkimizda":aboutt.objects.first()
    }
    return render(request,"admin/aboutList.html",context)

@login_required(login_url="login")
def aboutUpdate(request,id):
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    kontrol=get_object_or_404(aboutt,id=id)
    try:
        form=aboutForm(request.POST or None,request.FILES or None,instance=kontrol)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Hakkımızda bilgilerini güncelleme işlemi başarılı bir şekilde gerçekleşti..')
            return redirect("aboutList")
    except Exception as hata:
        messages.add_message(request,messages.WARNING,'Hakkımızda bilgilerini güncelleme işlemi sırasında hata meydana geldi!',hata)
    context={
        "form":form,
        "value":kontrol
    }
    return render(request,"admin/aboutUpdate.html",context)

#---------------------ADMİN--ABOUT---------------------------------


#-----------------------SEARCH-------------------------------------

def search(request):
    gelendeger=request.GET.get("value")
    if gelendeger:
        sorgu=blog.objects.filter(title__contains=gelendeger) # eğer gelendeger tablo içerisinde varsa,sorgudan dönen sonucu döndür
        return render(request,"blog/search.html",{"sonuc":sorgu})
        
        
#-----------------------404-NOT-FOUND------------------------------

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


#--------------------------COMMENT---------------------------------


def commentList(request):
    sorgu=comment.objects.all().order_by("comment_date")
    context={
        "yorumlar":sorgu
    }
    return render(request,"admin/commentList.html",context)


def commentInsert(request,id): # id; blogDetay URL'sinden geliyor
    if request.user.is_authenticated and request.user.is_staff: 
        return redirect("index")
    if request.method=="POST":
        _blog=get_object_or_404(blog,id=id)
        _gelenveri1=request.POST["nameSurname"]
        _gelenveri2=request.POST["email"]
        _gelenveri3=request.POST["message"]
        newComment=comment(nameSurname=_gelenveri1,message=_gelenveri3,email=_gelenveri2,blog=_blog)
        newComment.status=True
        newComment.save()
    return redirect(reverse('blogDetails',kwargs={"id":id})) # Dinamik URL yönlendirmesi yaparken reverse kullanırız => localhost/blogDetails/5
    



