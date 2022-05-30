from django.contrib import admin
from .models import category,blog,author,comment

# sınıf'a admin yetkilerine sahip olma özelliği tanımladık.
class adminCategory(admin.ModelAdmin): 
    list_display=['name','description','status']
    list_display_links=["name"]
    list_editable=["status"]

admin.site.register(category,adminCategory)


class adminBlog(admin.ModelAdmin):
    list_display=['title','fileURL','release_date','status','categories','select_author',]
    list_display_links=["title"]
    list_editable=["status"]
    prepopulated_fields = {"slug": ("title",)} #  title alanına girilen değere göre,tablodaki slug alanı otomatik olarak doldurulcak.
    
    # N-N ilişki tipi kullanıldığında,admin-Blog modülü içerisinde ilişkili olan kolonu göstermek istediğimizde hata alırız,fonksiyon tanımlayarak ilgili değeri gösterebiliriz.
    def select_author(self,gelendeger): # ilgili model'e ait kolonları alabiliriz, 
        yazdir=""
        for item in gelendeger.authors.all(): # model içerisinde tanımlanan authors kolonu
            yazdir+=item.nameSurname+ " "
        return yazdir
        
    
admin.site.register(blog,adminBlog)


class adminAuthor(admin.ModelAdmin):
    list_display=['nameSurname','birthday','status',]
    list_display_links=["nameSurname"]
    list_editable=["status"]

admin.site.register(author,adminAuthor)


class adminComment(admin.ModelAdmin):
    list_display=['nameSurname','email','comment_date','status','blog']
    list_display_links=["nameSurname"]
    list_editable=["status"]

admin.site.register(comment,adminComment)