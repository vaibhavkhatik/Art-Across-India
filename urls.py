
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about_us/',views.about,name='about_us'),
    path('contact_us/',views.contact,name='contact_us'),
    path('contact_us/about_us/',views.contact,name='contact_us'),
    path('registration/',views.registration,name='registration'),
    path('productView/<email>/<int:id>',views.productView,name='productView'),
    path('productView/<int:id>',views.homePageProductView,name='productView'),
    path('artist/artist_homepage/', views.productView, name='artist_homepage'),
    path('login/', views.login, name='login'),
    path('login/login1/', views.login1, name='login1'),
    path('upload_art/<email>/', views.upload_art, name='upload'),
    path('my_art/<email>/', views.myArt, name='myArt'),
    path('cart/<email>/', views.cart,name="cart"),
    path('cart/<email>/<int:id>/', views.remove_from_cart,name="cart"),
    path('buy_now/<email>/<int:id>/', views.Buy_now,name="buy_now"),
    path('contact_artist/<int:id>/', views.contact_artist,name="contact_artist"),
    path('addToCart/<email>/<int:id>/',views.addToCart,name='addToCart'),
    path('artist/<email>/',views.artist,name="artist"),
    path('view_profile/<email>/' ,views.viewProfile,name="viewProfile"),
    path('edit_profile/<email>/', views.editProfile,name="editProfile"),
    path('user/<email>/',views.user_login,name="user"),
    path('update_art/<email>/<int:id>/',views.update_art,name="update_art"),
    path('remove_art/<email>/<int:id>/',views.rmoveArt,name="remove_art"),
    path('order_success/<email>/',views.orderSuccess,name="orderSuccess"),
    path('order_detail/<email>/',views.orderDetail,name="orderDetail"),
    path('myOrder/<email>/',views.myOrders,name="myOrders"),
    path('contact_artist/<email>/<int:id>/', views.contact_artist2,name="contact_artist"),


]