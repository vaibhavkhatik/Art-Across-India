from django.db import models

# Create your models here.
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    art_name=models.CharField(max_length=100,default="")
    art_descripion=models.CharField(max_length=500,default="")
    art_price=models.IntegerField(default=0)
    art_category=models.CharField(max_length=50,default="")
    art_subcategory=models.CharField(max_length=50,default=0)
    art_date=models.DateField(default=2021-1-1)
    image=models.ImageField(upload_to='art_shop/images',null=True)
    def __str__(self):
        return self.art_name

class About(models.Model):
    name=models.CharField(max_length=50,default="")
    image=models.ImageField(upload_to='art_shop/images',default="")
    email=models.CharField(max_length=100,default="")
    description=models.CharField(max_length=100,default="")
    linkdin=models.CharField(max_length=200,default="")
    def __str__(self):
        return self.name
class Contact(models.Model):
    form_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=100,default="")
    text=models.CharField(max_length=1000,default="")
    rating=models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Registration1(models.Model):
    profile_image=models.ImageField(upload_to='art_shop/images',null=True)
    first_name=models.CharField(max_length=30,default="")
    last_name=models.CharField(max_length=30,default="")
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50,default="")
    address=models.CharField(max_length=300,default="")
    contact_tel=models.CharField(max_length=10,default="")
    gender=models.CharField(max_length=20,default="")
    user_type=models.CharField(max_length=20,default="")
    def __str__(self):
        return  self.first_name

class My_art(models.Model):
    art_id=models.IntegerField(default=0)
    artist_email=models.EmailField(max_length=100)
    def __str__(self):
        return self.artist_email
class AddToCart(models.Model):
    art_id=models.IntegerField(default=0)
    user_email=models.EmailField(max_length=100)
    def __str__(self):
        return self.user_email
class Orders(models.Model):
    artist_email=models.EmailField(max_length=100)
    art_id=models.IntegerField(default=0)
    user_email=models.EmailField(max_length=100)
    address=models.CharField(max_length=300,default="")
    contact_num=models.CharField(max_length=100)
    payment_type=models.CharField(max_length=50,default="")
    paid=models.BooleanField(default=False)
    status=models.CharField(max_length=30,default="pending")

    def __str__(self):
        return self.user_email

class ArtFeedback(models.Model):
    id=models.AutoField
    artist_email=models.EmailField(max_length=100)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    feedback=models.CharField(max_length=1000);
    def __str__(self):
        return self.name

