from django.contrib import admin
from myModel import models

# Register your models here.
#admin.site.register([Users, UsersLocation, Contact,Equip,HouseMemory,HousePic,Icon,Orders,
#                     House,HouseDiscount,HouseDisplay,HouseEquip,HouseIcon,HouseLabel])

class UsersAdmin(admin.Modeladmin):
    list_display = [f.name for f in models.Users._meta.fields]

admin.site.register(models.Users,UsersAdmin)