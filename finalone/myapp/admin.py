from django.contrib import admin
from .models import Advertise,Location,Category,UserDetail,Favourites,Messages
admin.site.register(Advertise)
admin.site.register(Category)
admin.site.register(UserDetail)
admin.site.register(Location)
admin.site.register(Favourites)
admin.site.register(Messages)
# Register your models here.
