from django.contrib import admin
from myModel.models import Users,UsersLocation,Contact,Equip,House,HouseDiscount,\
    HouseDisplay,HouseEquip,HouseIcon,HouseLabel,HouseMemory,HousePic,Icon,Orders

# Register your models here.
#admin.site.register([Users, UsersLocation, Contact,Equip,HouseMemory,HousePic,Icon,Orders,
#                     House,HouseDiscount,HouseDisplay,HouseEquip,HouseIcon,HouseLabel])

class UsersAdmin(admin.ModelAdmin):
    list_display = ['uid']

admin.site.register(Users,UsersAdmin)