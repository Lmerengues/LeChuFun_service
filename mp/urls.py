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
 
from . import view,home,detail,form,login,order,pay,index,contact,success,res

from django.contrib import admin
import settings  
 
urlpatterns = [
    url(r'^$',view.index),
    url(r'^index$', index.index),
    url(r'^price_index$', index.price_index),
    url(r'^hello$', pay.test),
    url(r'^res_index$', res.index),
    url(r'^admin/', admin.site.urls),
    url(r'^detail$', detail.index),
    url(r'^form$', form.index),
    url(r'^form_submit$', form.submit),
    url(r'^login$',login.login),
    url(r'^order$',order.index),
    url(r'^check_date$',order.check_date),
    url(r'^check_time$',order.check_time),
    url(r'^contact$',contact.index),
    url(r'^cal_price$',order.cal_price),
    url(r'^contact_submit$',contact.submit),
    url(r'^pay$',pay.index),
    url(r'^pay_notify$',pay.notify),
    url(r'^success$',success.index),
    url(r'^like$',detail.like),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT }),  
]
