from django.contrib import admin
from myModel.models import Users,UsersLocation,Contact,Equip,House,HouseDiscount,\
    HouseDisplay,HouseEquip,HouseIcon,HouseLabel,HouseMemory,HousePic,Icon,Orders

# Register your models here.
#admin.site.register([Users, UsersLocation, Contact,Equip,HouseMemory,HousePic,Icon,Orders,
#                     House,HouseDiscount,HouseDisplay,HouseEquip,HouseIcon,HouseLabel])

class UsersAdmin(admin.Modeladmin):
    list_display = [f.name for f in Users._meta.fields]

admin.site.register(Users,UsersAdmin)