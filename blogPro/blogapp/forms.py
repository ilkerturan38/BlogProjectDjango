import hashlib
from django import forms
from django.contrib.auth.hashers import make_password,check_password,MD5PasswordHasher
import hashlib


from .models import author, category,blog,aboutt

class categoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields=["name","description"] # __all__ model içerisindeki tüm alanlar gelir.
        error_messages={
            "name":{
                "required":"Bu alan Boş geçilemez.", # Model içerisinde tanımlanmasa bile,varsayılan olarak required=True gelir.
                "max_length":"En fazla 50 karakter girebilirsiniz!"
            }
        }
        labels={
            "description":"Kategori Detayı"
        }
        
        # ModelForm ile validasyon işlemi yapıldı ama çalışmadı!
        def clean(self):
            #cleaned_data=super().clean()
            super(categoryForm, self).clean()
            nname=self.cleaned_data.get('name')
            if len(nname) < 5:
                raise forms.ValidationError("en az 5 karakter giriniz!")
            return nname


class blogForm(forms.ModelForm):
    class Meta:
        model=blog
        fields=["title","description","fileURL"]



class aboutForm(forms.ModelForm):
    class Meta:
        model=aboutt
        fields=["description1","description2","imageURL1","imageURL2"]
        widgets = {
            'description1': forms.Textarea(attrs={'rows': 5}),
            'description2': forms.Textarea(attrs={'rows': 5}),
        }


class authorForm(forms.ModelForm):
    class Meta:
        model=author
        fields=["username","password","nameSurname","birthday","imageURL"]
        widgets = {
            'password': forms.PasswordInput,
        }


# ModelForm ile oluşturulan formlar'da clean metodu çalışmıyor,yani hiçbir validasyon işlemi uygulanmıyor.

