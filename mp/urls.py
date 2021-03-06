"""mp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
 
from . import detail,login,order,pay,index,contact,success,res,push,mail,view,\
    qrcode,ruc,k_index,k_detail,k_place,k_order,k_ticket,k_contact,k_login,k_pay,k_list,k_food,k_view,k_add,k_del,\
    m_detail,m_form,m_home,m_login,m_order,m_pay,m_view,k_qrcode,sleepy


from django.contrib import admin
import settings  
 
urlpatterns = [
    url(r'^$',view.index),
    url(r'^add$', view.add),
    url(r'^addHouseHandle$', view.addHouseHandle),
    #url(r'^equips$', view.equips),
    #url(r'^icons$', view.icons),

    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),


    url(r'^index$', index.index),
    url(r'^index_price$', index.index_price),
    url(r'^index_location$', index.index_location),

    url(r'^detail$', detail.index),

    url(r'^login$',login.login),

    
    url(r'^order$',order.index),

    url(r'^check_date$',order.check_date),
    url(r'^check_time$',order.check_time),
    url(r'^cal_price$',order.cal_price),

    url(r'^contact$', contact.index),
    url(r'^contact_submit$', contact.submit),

    url(r'^pay$', pay.index),
    url(r'^pay_notify$', pay.notify),

    url(r'^push', push.index),

    url(r'^mail$', mail.index),

    url(r'^success$',success.index),

    url(r'^res_index$', res.index),

    url(r'^getqrcode$', qrcode.index),
    url(r'^kgetqrcode$', k_qrcode.index),

    url(r'^ruc$', ruc.home),

    # here comes klook!

    url(r'^kindex$', k_index.index),
    url(r'^kdetail$', k_detail.index),
    url(r'^kcomment$', k_detail.comment),
    url(r'^kplace$', k_place.index),
    url(r'^korder$', k_order.index),
    url(r'^kticket$', k_ticket.index),
    url(r'^kcreate_ticket$', k_ticket.create),
    url(r'^kcontact$', k_contact.index),
    url(r'^kcontact_submit$', k_contact.submit),
    url(r'^klogin$', k_login.login),
    url(r'^kpay$', k_pay.index),
    url(r'^kpay_notify$', k_pay.notify),

    url(r'^kplace_index$', k_place.detail),
    url(r'^klist$', k_list.index),
    url(r'^kfood_list$', k_food.index),
    url(r'^korder_list$', k_order.list),
    url(r'^krefund$', k_order.refund),
    url(r'^kadd$', k_view.add),
    url(r'^kaddHouseHandle$', k_view.addHouseHandle),


    url(r'^kactivity$', k_view.activity_list),
    url(r'^krule$', k_view.activity_rule),
    url(r'^kinstruction$', k_view.activity_instruction),
    url(r'^kuse$', k_view.activity_use),
    url(r'^krefundadd$', k_view.activity_refund),
    url(r'^kimage$', k_view.activity_image),
    url(r'^kpackage$', k_view.activity_package),
    url(r'^prule$', k_view.package_rule),
    url(r'^pticket$', k_view.package_ticket),
    url(r'^addcity$', k_view.city_add),


    url(r'^add_activity$', k_add.add_activity),
    url(r'^add_city$', k_add.add_city),
    url(r'^add_rule$', k_add.add_rule),
    url(r'^add_ins$', k_add.add_ins),
    url(r'^add_refund$', k_add.add_refund),
    url(r'^add_use$', k_add.add_use),
    url(r'^add_image$', k_add.add_image),
    url(r'^add_prule$', k_add.add_prule),
    url(r'^add_pticket$', k_add.add_pticket),
    url(r'^add_package$', k_add.add_package),

    url(r'^del_activity$', k_del.del_activity),


    url(r'^hot_update$', k_add.hot_update),
    url(r'^theme_update$', k_add.theme_update),
    url(r'^rec_update$', k_add.rec_update),

    url(r'^kcity$', k_view.city),

    url(r'^place_hot_update$', k_add.place_hot_update),

    url(r'^m_hello$', m_pay.test),
    #url(r'^admin/', admin.site.urls),
    url(r'^m_home$', m_home.index),
    url(r'^m_detail$', m_detail.index),
    url(r'^m_form$', m_form.index),
    url(r'^m_form_submit$', m_form.submit),
    url(r'^m_login$',m_login.login),
    url(r'^m_order$',m_order.index),
    url(r'^m_pay$',m_pay.index),
    url(r'^m_pay_notify$',m_pay.notify),
    url(r'^m_like$',m_detail.like),

    url(r'^sleepy$',sleepy.index),
    # url(r'^hello$', pay.test),

    # url(r'^form$', form.index),
    # url(r'^form_submit$', form.submit),

    # url(r'^like$',detail.like),


]



