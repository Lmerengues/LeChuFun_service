from django.contrib import admin
#from myModel.models import Users,UsersLocation,Contact,Equip,House,HouseDiscount,\
#    HouseDisplay,HouseEquip,HouseIcon,HouseLabel,HouseMemory,HousePic,Icon,Orders

from myModel import models as mm
# Register your models here.
#admin.site.register([Users, UsersLocation, Contact,Equip,HouseMemory,HousePic,Icon,Orders,
#                     House,HouseDiscount,HouseDisplay,HouseEquip,HouseIcon,HouseLabel])

class UsersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.Users._meta.fields]

class UsersLocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.UsersLocation._meta.fields]


admin.site.register(mm.Users,UsersAdmin)
admin.site.register(mm.UsersLocation,UsersLocationAdmin)