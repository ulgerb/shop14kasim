from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q # and('&') or('|') komutları için kullanılır 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.


def Query(request):
    query = request.GET.get('q')
    if query:
        cards = Card.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)).distinct()  # benzersiz olanları getir
        return cards
    else:
        cards = Card.objects.all().order_by("-id")
        return cards
        

def index(request):
    cards = Card.objects.all().order_by("-id")
    cards_r = Card.objects.all().order_by("?")[:6] # sıralama yapmak için kullanılır
    categorys = Category.objects.all()
    userinfo = ''
    if request.user.is_authenticated:
        userinfo =Userinfo.objects.get(user = request.user.id) # sadece girişli kullanıcının bilgisi geliceği için get kullandık (tek obje geliceği için)
    
    cards = Query(request)
    pagetitle = 'Anasayfa'
    context = {
        "cards":cards,
        "cards_r":cards_r,
        "categorys": categorys,
        'userinfo': userinfo,
        'pagetitle':pagetitle,
    }
    
    return render(request,'index.html',context)

def Product(request,id='all'):
    cards = Card.objects.all().order_by("-id")
    cards_r = Card.objects.all().order_by("?")[:6] # sıralama yapmak için kullanılır
    userinfo = ''
    if request.user.is_authenticated:
        userinfo = Userinfo.objects.get(user=request.user.id)
    
    print(request.path)
    
    # search
    cards = Query(request)
    # kategori start
    categorys = Category.objects.all()
    pagetitle = 'Tüm Ürünler'
    if id.isnumeric(): # id içindeki sayılardan mı oluşuyor?
        cards = Card.objects.filter(category=id)
        pagetitle = Category.objects.get(id=id)
    # kategori end
    
    # paginator
    paginator = Paginator(cards, 1) # Paginator(objeler, sayfayı kaçar bölüceksin)
    page_number = request.GET.get('page')
    cards = paginator.get_page(page_number)
    
    context = {
        "cards":cards,
        "cards_r":cards_r,
        "categorys": categorys,
        'userinfo': userinfo,
        'pagetitle': pagetitle,
    }
    
    return render(request,'products.html',context)


@login_required(login_url='/login/')
def Detail(request,id):
    card = Card.objects.get(id=id) # TEK BİR ÜRÜN GETİR
    comments = Comment.objects.filter(card=id) # birden fazla ürün döndürür ve filtreler
    userinfo = ''
    if request.user.is_authenticated:
        userinfo = Userinfo.objects.get(user=request.user.id)

    query = request.GET.get('q')
    if query:
        cards = Query(request)
        return render(request,'products.html',{'cards':cards})
        
    if request.method == "POST":
        name = request.POST["name"]
        comment = request.POST["comment"]
        
        comm = Comment(name=name, text=comment, card=card)
        comm.save()
    pagetitle = card.title
    context={
        "card":card,
        "comments":comments,
        'userinfo': userinfo,
        'pagetitle': pagetitle,
    }
    return render(request,'detail.html',context)

# ==========================
# MYPRODUCT
# ==========================

def myProducts(request):
    products = Card.objects.filter(user=request.user.id)
    
    context = {
        'products': products
    }
    return render(request,'product/myproducts.html',context)

def createProduct(request):
    
    if request.method == "POST":
        print(request.POST)
        title = request.POST['title']
        text = request.POST['text']
        category = request.POST['category']
        priece = request.POST['priece']
        image = request.FILES['image']

        card = Card(title=title, text=text, priece=priece, image=image, user=request.user)
        card.save()
        
    return render(request,'product/create.html')






# ==========================
# USER
# ==========================
# KAYDOL
messeges2 = None
def registerUser(request):
    global messeges2
    
    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
            if User.objects.filter(username=username).exists(): # exists varsa true döndürür
                messeges = "Bu kullanıcı adı daha önceden alınmış!"
                return render(request, 'users/register.html', {"messeges": messeges})
            
            elif User.objects.filter(email=email).exists():
                messeges = "Bu email zaten başkası tarafından kullanılıyor!"
                return render(request, 'users/register.html', {"messeges": messeges})
            
            else:
                # KAYDOL start
                user = User.objects.create_user(first_name=name, last_name=surname, email=email, username=username, password=password1)
                user.save()
                # KAYDOL end
                messeges2 = "Kaydınız başarıyla tamamlanmıştır"
                return redirect('loginUser')
                
    return render(request, 'users/register.html', {'pagetitle':'Kaydol'})

# ip 111 kullanıcının deneme hakkı = 5
# GİRİŞ YAP
def loginUser(request):
    
    global messeges2
    if messeges2 is not None:
        return render(request, 'users/login.html', {"messeges2": messeges2})
    
    if request.method == "POST":
        # ip111 -= 1
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messeges = "Kullanıcı adı veya şifre hatalı!"
            return render(request, 'users/login.html',{"messeges":messeges})
        
    return render(request, 'users/login.html', {'pagetitle':'Giriş Yap'})

# ÇIKIŞ YAP
def logoutUser(request):
    logout(request)
    return redirect('index')

# ŞİFRE DEĞİŞTİR
def changePassword(request):
    userinfo = ''
    if request.user.is_authenticated:
        userinfo = Userinfo.objects.get(user=request.user.id)
    if request.method == "POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1==password2:
            user = User.objects.get(username=request.user)
            user.set_password(password1)
            user.save()
            logout(request)
            return redirect('loginUser')
    
    context={
        "userinfo":userinfo,
        'pagetitle':'Şifre Değiştir'
    }
    return render(request,'users/change.html',context)
    