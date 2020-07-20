from django.db import models
from django.contrib.auth.models import  User
from datetime import datetime
# Create your models here.



class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_info = models.CharField(max_length=500, null=True, blank=True)
    user_fname = models.CharField(max_length=100, null=True, blank=True)
    user_lname = models.CharField(max_length=100, null=True, blank=True)
    user_image = models.ImageField(upload_to='images/user_images', null=True, blank=True,
                                   help_text="Upload only .png and jpg",default="images/user_images/default.jpg")
    user_city = models.CharField(max_length=100, null=True, blank=True)
    user_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table="user_detail"
        verbose_name="User Detail"
        managed=True


class Location(models.Model):

    location_name = models.CharField(max_length=50, blank=True, null=True)
    current_user = models.IntegerField()
    def __str__(self):
        return self.location_name
    
    

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        managed = True


class Favourites(models.Model):
    ad_id = models.IntegerField()
    user_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ad_id

    class Meta:
        db_table = "favourite"
        verbose_name = "Favourite"
        managed = True


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=True, null=True)
    current_user = models.IntegerField()
    category_image = models.ImageField(upload_to='images/cat_images', null=True, blank=True, help_text="Upload on;y .png and.jpg")

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category"
        verbose_name = "Categorie"
        managed = True

class Advertise(models.Model):
    user=models.IntegerField()
    title=models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=300)
    image=models.ImageField(upload_to='images/ad_images',null=True,blank=True,help_text="Upload only .png and.jpg")
    image1=models.ImageField(upload_to='images/ad_images',null=True,blank=True,help_text="Upload only .png and.jpg")
    image2=models.ImageField(upload_to='images/ad_images',null=True,blank=True,help_text="Upload only .png and.jpg")
    location=models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    contact=models.BigIntegerField(blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    posted_on=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "postad"
        verbose_name = "Post Ad"
        managed = True

class Messages(models.Model):
    subject=models.CharField(max_length=200,blank=True,null=True)
    message = models.CharField(max_length=500,null=True)
    ad_id=models.ForeignKey(Advertise, blank=True, null=True, on_delete=models.CASCADE)
    s_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='sid')
    r_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='rid')
    posted_on=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "messages"
        verbose_name = "Messages"
        managed = True

