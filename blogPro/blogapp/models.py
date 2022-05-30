from tabnanny import verbose
from tkinter import CASCADE
from tokenize import blank_re
from django.db import models
from ckeditor.fields import RichTextField
from django.forms import CharField, ImageField
from django.utils.text import slugify

from autoslug import AutoSlugField

class category(models.Model):
    name=models.CharField(max_length=100,verbose_name="Kategori Adı")
    description=RichTextField(max_length=500,verbose_name="Kategori Detayı",blank=False, null=False)
    status=models.BooleanField(default=True,verbose_name="Durum",blank=True, null=False)
    slug=models.SlugField(null=False,blank=True,db_index=True,unique=True,editable=True)
    
    def __str__(self) :
        return self.name

    # category Modeli'ne ait save metodunu override ettik.(Örn; Kayıt eklerken newCategory=kodlar newCategory.save dediğimizde ki, save metodunu override etmiş olduk.)
    def save(self,*args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args, **kwargs)


class author(models.Model):
    nameSurname=models.CharField(max_length=50,verbose_name="Ad-Soyad",blank=True, null=True)
    birthday=models.DateField(null=True, blank=True,verbose_name="Doğum Tarihi")
    status=models.BooleanField(default=True,verbose_name="Durum",blank=True, null=True)
    imageURL=models.ImageField(verbose_name="Resim",blank=False,null=False)
    about=models.TextField(verbose_name="Yazar Biyografisi", max_length=250,null=True,blank=True)
    blogs=models.ManyToManyField('blog',related_name="authorBlog") # through='ortak' : her iki tablodaki ManytoMany alanlarına Bu özelliği verirsek,Sadece bizim sonradan oluşturduğumuz ortak isimli tablo içerisine kayıtlar eklenir.
    username=models.CharField(max_length=30,verbose_name="Kullanıcı Adı",blank=False,null=False)
    password=models.CharField(max_length=30,verbose_name="Şifre",blank=False,null=False)
    
    def __str__(self):
        return self.nameSurname


class blog(models.Model):
    title=models.CharField(max_length=100,verbose_name="Başlık",blank=False, null=True)
    description=RichTextField(verbose_name="Açıklama",blank=False,null=True)
    fileURL=models.FileField(upload_to="blog",verbose_name="Dosya",blank=True, null=True)
    release_date=models.DateField(auto_now_add=True,null=True,blank=True,verbose_name="Yayınlanma Tarihi")
    status=models.BooleanField(default=True,verbose_name="Durum",blank=True, null=True)
    categories=models.ForeignKey(category,on_delete=models.SET_NULL,null=True,blank=False) # Her Bloğun Yalnızca,Bir Kategorisi olur.Çok olan tarafa Foreign Key yapısı eklemiyoruz.
    authors=models.ManyToManyField('author',related_name="blogAuthor") # through='ortak'
    slug=AutoSlugField(populate_from='title',null=False,blank=False,db_index=True,unique=True,editable=True)

    # Model içerisinde manyToMany ilişkisini kurarken verdiğimiz ilişki adı admin kısmında object(1) olarak gözükebilir. 
    # Çözümü : karşı modelde alınan ilişkiye ait değer __str__(self) ile return edilmeli.

    def __str__(self):
        # return self.title  # tek,tek kayıt silmek istediğimizde bu yöntemi kullanırız.
        return "(%r, %r, %r)" (self.title, self.description, self.categories)  # admin panelinde birden fazla kayıt silmek istediğimizde bu yöntemi kullanırız
        

class aboutt(models.Model):
    description1=models.CharField(verbose_name="Açıklama 1",null=False,blank=False,max_length=250)
    description2=models.CharField(verbose_name="Açıklama 2",null=False,blank=False,max_length=250)
    imageURL1=models.ImageField(verbose_name="Resim 1",null=False,blank=False)
    imageURL2=models.ImageField(verbose_name="Resim 2",null=False,blank=False)


class comment(models.Model):
    nameSurname=models.CharField(max_length=50,verbose_name="Ad-Soyad",blank=False,null=False)
    email=models.EmailField(max_length=50,verbose_name="E-mail",blank=False,null=False)
    message=models.CharField(max_length=500,verbose_name="Mesaj",blank=False,null=False)
    comment_date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True,verbose_name="Durum",blank=False, null=False)
    blog=models.ForeignKey(blog,on_delete=models.CASCADE,related_name="comments") # related-name = Ters-İlişki yaptığımızda gerekli. blog.comment.all()

    def __str__(self) :
        return self.blog


class ortak(models.Model):
    authorX=models.ForeignKey(author,on_delete=models.CASCADE,null=False,blank=False)
    blogY=models.ForeignKey(blog,on_delete=models.CASCADE,null=False,blank=False)





    






    