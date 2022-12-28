"""mediamodel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# SQL veri tabanından gelen resim dosyaları için
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path
from appMy.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('products/<id>/', Product, name='product'),
    path('detay/<id>/',Detail, name='detail'),
    
    # My Products
    path('myproducts/', myProducts, name='myProducts'), # ürünlerim
    path('createproduct/', createProduct, name='createProduct'), # ürün oluştur
    path('updateproduct/<id>/', updateProduct, name='updateProduct'), # ürün oluştur
    path('deleteproduct/<id>/', deleteProduct, name='deleteProduct'), # ürün sil
    
    # Users
    path('login/', loginUser, name='loginUser'), # giriş yap
    path('register/', registerUser, name='registerUser'), # kaydol
    path('logout/', logoutUser, name='logoutUser'), # çıkış yap
    path('changepassword/', changePassword, name='changePassword'), # şifre değiştir
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
