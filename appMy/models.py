from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(("Kategori Adı"), max_length=50)

    def __str__(self):
        return self.name
    

class Card(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE,null=True)
    title = models.CharField(("Card Başlık"), max_length=100)
    text = models.TextField(("Card Yazısı"))
    image1 = models.FileField(("Card Resimi 1"), upload_to='', max_length=100, null=True)
    image2 = models.FileField(("Card Resimi 2"), upload_to='', max_length=100, null=True, blank=True)
    image3 = models.FileField(("Card Resimi 3"), upload_to='', max_length=100, null=True, blank=True)
    priece = models.IntegerField(("Ürün Fiyatı"), null=True)
    date_now = models.DateTimeField(("Paylaşım Zamanı"), auto_now_add=True)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    card = models.ForeignKey(Card, verbose_name=("Ürünler"), on_delete=models.CASCADE, null=True) # hangi ürüne yorum yapılcak
    name = models.CharField(("Ad Soyad"), max_length=50)
    text = models.TextField(("Yorum"), max_length=300)
    date_now = models.DateTimeField(("Yorum Zamanı"),  auto_now_add=True, null=True) 
    
    def __str__(self) :
        return self.card.title
    
class Userinfo(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    image =models.FileField(("Profil"), upload_to='', max_length=100, null=True, blank=True, default='new.jpg')
    address = models.CharField(("Adres"), max_length=150, null=True, blank=True)