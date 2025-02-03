import math
from django.shortcuts import render,redirect
from django.db import connection
from django.http import  HttpResponse

import razorpay
from .models import Product, About, Contact, Registration1, Orders, AddToCart, My_art, ArtFeedback
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ProductForm
from django.contrib.auth.models import User,auth
# Create your views here.

def index(request):
    product=Product.objects.raw("select art_category,id from art_shop_product")
    allprod=[]
    s=set()
    for i in product:
        s.add(i.art_category)
    for cat in s:
        prod=Product.objects.raw("select * from art_shop_product where art_category=%s",[cat])
        n=len(prod)
        nSlides = n // 4 + math.ceil(n / 4 - n // 4)
        allprod.append([prod,range(1,nSlides),nSlides])
    nprod={'allprod':allprod}
    return render(request,'art_shop/index.html',nprod)


def about(request):
    prod=About.objects.raw('select * from art_shop_about')
    allprod={'allprod':prod}
    return render(request,'art_shop/about.html',allprod)

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name',"")
        email = request.POST.get('email', "")
        text = request.POST.get('text', "")
        rating = request.POST.get('rating', 0)
        print(name)
        print(email)
        print(text)
        print(rating)
        with connection.cursor() as cursor:
            cursor.execute("insert into art_shop_contact(name,email,text,rating) values(%s,%s,%s,%s)",[name,email,text,rating])
    return render(request,'art_shop/contact.html')


def registration(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name',"")
        last_name=request.POST.get('last_name',"")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        contact = request.POST.get('phone', "")
        password1 = request.POST.get('password1', "")
        password2 = request.POST.get('password2', "")
        gender = request.POST.get('gender', "")
        user_type = request.POST.get('user_type', "")


        mail=f'hello {first_name} {last_name}  Welcome to art across india'

        msearch=Registration1.objects.filter(email=email)

        if password1== password2 and len(msearch)==0:
            send_mail('Successful Registration to Art across india',
                      mail,
                      'kulkarnishubham228@gmail.com',
                      [email]
                      )
            with connection.cursor() as cursor:
                cursor.execute("insert into art_shop_registration1(first_name,last_name,email,password,address,contact_tel,gender,user_type) values(%s,%s,%s,%s,%s,%s,%s,%s)",[first_name,last_name,email,password1,address,contact,gender,user_type])
            messages.info(request, "You are Successfully register to art across india ")
            return render(request, 'art_shop/login.html')
        else:
            messages.info(request,"Email id is already Register")
            return render(request,'art_shop/registration.html')
    return render(request,'art_shop/registration.html')

def productView(request,email,id):
    prod = Product.objects.raw("select * from art_shop_product where id=%s", [id])
    cat=prod[0].art_category
    allprod = Product.objects.raw("select * from art_shop_product where art_category=%s", [cat])

    prod1=prod[0]
    return render(request,'art_shop/productView.html',{'prod':prod1,'allprod':allprod,'email':email})


def homePageProductView(request,id):
    prod = Product.objects.raw("select * from art_shop_product where id=%s", [id])
    cat=prod[0].art_category
    allprod = Product.objects.raw("select * from art_shop_product where art_category=%s", [cat])
    prod1=prod[0]
    return render(request,'art_shop/productView.html',{'prod':prod1,'allprod':allprod})
def upload_art(request,email):
    form = ProductForm()
    if request.method == "POST":
        name=request.POST.get('name',"")
        price=request.POST.get('price',0)
        description=request.POST.get('description',"")
        category=request.POST.get('category',"")
        sub_category=request.POST.get('sub',"")
        image=request.FILES.get('file',"")
        date=datetime.date.today()
        image1=request.FILES.get('file')
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        print(email)
        print(name)
        print(price)
        print(description)
        print(category)
        print(sub_category)
        print(image)
        print(date)
        mm=Product(art_name=name,art_descripion=description,art_price=price,art_category=category,art_subcategory=sub_category,art_date=date,image=image)
        mm.save()
       # with connection.cursor() as cursor:
         #   cursor.execute( "insert into art_shop_product(art_name,art_descripion,art_price,art_category,art_subcategory,art_date,image) values(%s,%s,%s,%s,%s,%s,%s)",[name,description,price,category,sub_category,date,image])
        n=Product.objects.filter(art_name=name)

        art_id=n[0].id
        with connection.cursor() as cursor:
            cursor.execute('insert into art_shop_my_art(art_id,artist_email) values(%s,%s)', [art_id, email])
        return redirect(f"/art_shop/artist/{email}/")
    return render(request,'art_shop/upload_art.html',{'form':form})
def login(request):
    return render(request,'art_shop/login.html')
def login1(request):
    product = Product.objects.raw("select art_category,id from art_shop_product")
    allprod = []
    s = set()
    for i in product:
        s.add(i.art_category)
    for cat in s:
        prod = Product.objects.raw("select * from art_shop_product where art_category=%s", [cat])
        n = len(prod)
        nSlides = n // 4 + math.ceil(n / 4 - n // 4)
        allprod.append([prod, range(1, nSlides), nSlides])
    nprod = {'allprod': allprod}
    email=request.POST.get('email',"")
    password=request.POST.get('password',"")
    if request.method=="POST":
        user1=Registration1.objects.filter(email=email,password=password)
        print(len(user1))
        if len(user1) !=0:
            if(user1[0].user_type=='User'):
                return redirect(f"/art_shop/user/{email}/")
            else:
                return redirect(f"/art_shop/artist/{email}/")
        else:
            messages.info(request,"Please Enter the Valid Email or Password")
            return render(request,'art_shop/login.html')

def myArt(request,email):
    print(email)
    prod_id=My_art.objects.raw('select * from art_shop_my_art where artist_email=%s',[email])
    list_prod_id=[]
    print(len(prod_id))
    for i in prod_id:
        m=i.art_id
        list_prod_id.append(m)
    print(len(list_prod_id))
    allArts=[]
    for s in list_prod_id:
        k=Product.objects.get(id=s)
        allArts.append(k)
    print(len(allArts))
    for m in allArts:
        print(m.art_name)
    return  render(request,'art_shop/my_arts.html',{'myArt':allArts})
def cart(request,email):
    return render(request,'art_shop/cart.html')
def remove_from_cart(request,id):
    return HttpResponse("hello")
def Buy_now(request,email,id):
    print(id)
    print(email)
    art=Product.objects.raw('select * from art_shop_product where id=%s',[id])
    artist=My_art.objects.filter(art_id=id)
    print(len(art))
    print(len(artist))
    artist1 = Registration1.objects.raw('select * from art_shop_registration1 where email=%s', [artist[0].artist_email])
    print(len(art))
    print(len(artist))
    if request.method=="POST":
        art_id=id
        first_name =  request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        payment_type =request.POST.get('payment')
        terms = request.POST.get('terms')
        buyer_email = request.POST.get('buyer_email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        print(buyer_email)
        print(address)
        print(contact)
        print(first_name)
        print(last_name)
        print(payment_type)
        print(terms)
        print(artist1[0].first_name)
        print(artist1[0].last_name)
        print(artist1[0].email)

        mm=Product.objects.get(id=id)
        ammount=mm.art_price *100
        if terms=="on" and payment_type=='1':
            c = razorpay.Client(auth=('rzp_test_SBlAtKAEsxsH9b', 'fnSC0ZTJoSVL1MmQ2WIgh9vX'))
            payment = c.order.create({'amount': ammount, 'currency': 'INR', 'payment_capture': '1'})
            print(len(payment))
            orders = Orders(art_id=art_id, user_email=email, artist_email=artist[0].artist_email, address=address,
                            contact_num=contact, payment_type=payment_type, paid=True)
            orders.save()
            return render(request,'art_shop/pay_now.html',{'art':art[0],'artist':artist1[0],'payment':payment,'email':email})

        if terms == "on" and payment_type == '2':
            orders = Orders(art_id=art_id, user_email=email, artist_email=artist[0].artist_email, address=address,
                            contact_num=contact, payment_type=payment_type, paid=False)
            orders.save()
            return render(request, 'art_shop/order_successful.html', {'art': art[0], 'artist': artist1[0],'email':email})


    return render(request,'art_shop/buy_now.html',{'art':art[0],'artist':artist1[0]})

def orderSuccess(request,email):
    return render(request,'art_shop/order_successful.html',{'email':email})

def contact_artist(request,id):
    artist1 = My_art.objects.filter(art_id=id)
    print(len(artist1))
    artist2 = Registration1.objects.filter(email=artist1[0].artist_email)
    if request.method=="POST":
        user_email=request.POST.get('email')
        user_name=request.POST.get('name')
        subject=request.POST.get('subject')
        feedback=request.POST.get('feedback')


        obj=ArtFeedback(email=user_email,name=user_name,subject=subject,feedback=feedback,artist_email=artist1[0].artist_email)
        obj.save()
        messages.info(request,"Successfully send your feedback/query to artist through mail he is conatct you soon!!!")
    return render(request,"art_shop/contact_to_artist.html",{'email':id,'artist':artist2[0]})

def addToCart(request,email,id):
    art=AddToCart.objects.raw('insert into art_shop_addtocart(art_id,user_email) values(%s,%s)',[id,email])
    return redirect(login1)

def user(request,email):
    return redirect("/")

def artist(request,email):
    prod_id = My_art.objects.raw('select * from art_shop_my_art where artist_email=%s', [email])
    list_prod_id = []
    allArts=[]
    print(prod_id)
    for i in prod_id:
        m = i.art_id
        list_prod_id.append(m)
        prod = Product.objects.raw("select * from art_shop_product where id=%s", [m])
        if len(prod)!=0:
            allArts.append(prod[0])
            print(prod[0].art_name)
            print(prod[0].art_price)
            print(prod[0].art_descripion)
            print(prod[0].art_category)
    return render(request, 'art_shop/artist.html', {'myArts': allArts,'user1': email})



def viewProfile(request,email):
    user=Registration1.objects.raw('select * from art_shop_registration1 where email=%s',[email])
    return render(request,'art_shop/view_profile.html',{'user':user[0]})


def editProfile(request,email):
    user = Registration1.objects.raw('select * from art_shop_registration1 where email=%s', [email])
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        contact_tel=request.POST.get('phone')
        address=request.POST.get('address')
        profile_image=request.FILES.get('file')
        m=Registration1.objects.raw('select * from art_shop_registration1 where email=%s',[email])
        m[0].first_name=first_name
        m[0].last_name=last_name
        m[0].contact_tel=contact_tel
        m[0].address=address
        m[0].profile_image=profile_image
        m[0].save()
        return redirect(f"/art_shop/view_profile/{email}/")
    return render(request,'art_shop/update_profile.html',{'user':user[0]})

def user_login(request,email):
    product = Product.objects.raw("select art_category,id from art_shop_product")
    allprod = []
    s = set()
    for i in product:
        s.add(i.art_category)
    for cat in s:
        prod = Product.objects.raw("select * from art_shop_product where art_category=%s", [cat])
        n = len(prod)
        nSlides = n // 4 + math.ceil(n / 4 - n // 4)
        allprod.append([prod, range(1, nSlides), nSlides])
    return render(request, 'art_shop/user_homepage.html', {'prod': prod, 'allprod': allprod, 'user1': email})

def update_art(request,email,id):
    m = Product.objects.get(id=id)
    if request.method == "POST":
        name=request.POST.get('name',"")
        price=request.POST.get('price',0)
        description=request.POST.get('description',"")
        category=request.POST.get('category',"")
        sub_category=request.POST.get('sub',"")
        image=request.FILES.get('file',"")
        date=datetime.date.today()
        m.art_name=name
        m.art_price=price
        m.art_descripion=description
        m.art_category=category
        m.art_subcategory=sub_category
        m.image=image
        m.save()
        return redirect(f"/art_shop/artist/{email}/")
    return render(request,'art_shop/update_art.html',{'art':m})


def rmoveArt(request,email,id):
    m = Product.objects.get(id=id)
    m.delete()
    n = My_art.objects.get(art_id=id)
    n.delete()
    return redirect(f"/art_shop/artist/{email}/")


def orderDetail(request,email):
    order=Orders.objects.filter(user_email=email)
    arts=[]
    m=0
    for i in order:
        obj=Product.objects.filter(id=i.art_id)
        n=order[m]
        arts.append([obj[0],n])
        m=m+1
    print(len(order))
    print(len(arts))
    return render(request,'art_shop/cart.html',{'arts':arts,'orders':order,'email':email})


def myOrders(request,email):
    order=Orders.objects.filter(artist_email=email)
    arts=[]
    m=0
    for i in order:
        obj=Product.objects.filter(id=i.art_id)
        n=order[m]
        arts.append([obj[0],n])
        m=m+1
    print(len(order))
    print(len(arts))
    return render(request,'art_shop/myOrders.html',{'arts':arts,'orders':order,'email':email})

def contact_artist2(request,email,id):
    artist1 = My_art.objects.get(art_id=id)
    artist2 = Registration1.objects.filter(email=artist1.artist_email)
    print(len(artist2))
    if request.method=="POST":
        user_email=request.POST.get('email')
        user_name=request.POST.get('name')
        subject=request.POST.get('subject')
        feedback=request.POST.get('feedback')
        obj=ArtFeedback(email=user_email,name=user_name,subject=subject,feedback=feedback,artist_email=artist1.artist_email)
        obj.save()

    return render(request,"art_shop/contact_to_artist.html",{'email':email,'artist':artist2[0]})