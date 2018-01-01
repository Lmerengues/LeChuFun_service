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

class ContactAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.Contact._meta.fields]

class EquipAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.Equip._meta.fields]

class HouseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.House._meta.fields]

class HouseDiscountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseDiscount._meta.fields]

class HouseDisplayAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseDisplay._meta.fields]

class HouseEquipAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseEquip._meta.fields]

class HouseIconAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseIcon._meta.fields]


class HouseLabelAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseLabel._meta.fields]

class HouseMemoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HouseMemory._meta.fields]

class HousePicAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.HousePic._meta.fields]


class IconAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.Icon._meta.fields]

class OrdersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in mm.Orders._meta.fields]


admin.site.register(mm.Users,UsersAdmin)
admin.site.register(mm.UsersLocation,UsersLocationAdmin)
admin.site.register(mm.Contact,ContactAdmin)
admin.site.register(mm.Equip,EquipAdmin)
admin.site.register(mm.House,HouseAdmin)
admin.site.register(mm.HouseDiscount,HouseDiscountAdmin)
admin.site.register(mm.HouseDisplay,HouseDisplayAdmin)
admin.site.register(mm.HouseEquip,HouseEquipAdmin)
admin.site.register(mm.HouseIcon,HouseIconAdmin)
admin.site.register(mm.HouseLabel,HouseLabelAdmin)
admin.site.register(mm.HouseMemory,HouseMemoryAdmin)
admin.site.register(mm.HousePic,HousePicAdmin)
admin.site.register(mm.Icon,IconAdmin)
admin.site.register(mm.Orders,OrdersAdmin)
