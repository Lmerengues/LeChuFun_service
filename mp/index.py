from django.http import HttpResponse

import json
from django.db import connections

import math

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def f2(a,b):
    if b['c']-a['c']<0:
        return 1
    else:
        return -1
'''
def index(request):
    cursor = connections['default'].cursor()
    cursor.execute(
        "select house.hno,htitle1,htitle2,hprice,htype,hpic from house,house_display where house.hno = house_display.hno and house_display.hflag = 1")
    raw = dictfetchall(cursor)
    cursor.close()
    for rawitem in raw:
        hno = rawitem['hno']
        lcursor = connections['default'].cursor()
        lcursor.execute(
            "select lname from house,house_label where house.hno = house_label.hno and house_label.hno = %s",
            (hno,))
        rawitem['labels'] = dictfetchall(lcursor)
        lcursor.close()

        icursor = connections['default'].cursor()
        icursor.execute(
            "select pno,purl from house,house_pic where house.hno = house_pic.hno and house_pic.hno = %s",
            (hno,))
        rawitem['images'] = dictfetchall(icursor)
        icursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response
'''

def index(request):
    flag =  0
    openid = request.GET['openid']

    if request.GET['latitude'] and request.GET['longitude'] and request.GET['speed'] and request.GET['accuracy']:
        his_lati = float(request.GET['latitude'])
        his_longi = float(request.GET['longitude'])
        his_speed = request.GET['speed']
        his_accuracy = request.GET['accuracy']

        cursor = connections['default'].cursor()
        cursor.execute("insert into Users_location values(%s,%s,%s,%s,%s,sysdate())",
                       (request.GET['openid'],his_lati,his_longi,his_speed,his_accuracy,))
        cursor.close()
        flag = 1

    openid = request.GET['openid']

    cursor = connections['default'].cursor()
    cursor.execute(
        "select house.hno,htitle1,htitle2,hprice,htype,hpic,hlongitude,hlatitude from house,house_display where house.hno = house_display.hno and house_display.hflag = 1 order by hvalue desc ")
    raw = dictfetchall(cursor)
    cursor.close()
    for rawitem in raw:
        hno = rawitem['hno']
        lcursor = connections['default'].cursor()
        lcursor.execute(
            "select lname from house,house_label where house.hno = house_label.hno and house_label.hno = %s",
            (hno,))
        rawitem['labels'] = dictfetchall(lcursor)
        lcursor.close()

        icursor = connections['default'].cursor()
        icursor.execute(
            "select pno,purl from house,house_pic where house.hno = house_pic.hno and house_pic.hno = %s",
            (hno,))
        rawitem['images'] = dictfetchall(icursor)
        icursor.close()
        if flag:
            delta_weidu = his_lati - float(rawitem['hlatitude'])
            delta_jingdu = his_longi - float(rawitem['hlongitude'])

            a = (delta_weidu * 3600) * 30.8
            b = (delta_jingdu * 3600) * 30.8 * math.cos(his_lati)
            c = math.sqrt(a * a + b * b)
            rawitem['c'] = c + 0.0
            if c < 1000:
                rawitem['distance'] = round(c)
                rawitem['danwei'] = 'm'
            else:
                rawitem['distance'] = round((c + 0.0) / 1000, 1)
                rawitem['danwei'] = 'km'

    #raw.sort(cmp=f2)
    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response


def index_price(request):
    flag = 0
    if request.GET['latitude'] and request.GET['longitude'] and request.GET['speed'] and request.GET['accuracy']:
        his_lati = float(request.GET['latitude'])
        his_longi = float(request.GET['longitude'])
        his_speed = request.GET['speed']
        his_accuracy = request.GET['accuracy']
        flag = 1

    openid = request.GET['openid']

    cursor = connections['default'].cursor()
    cursor.execute(
        "select house.hno,htitle1,htitle2,hprice,htype,hpic,hlongitude,hlatitude from house,house_display where house.hno = house_display.hno and house_display.hflag = 1 order by hprice ASC ")
    raw = dictfetchall(cursor)
    cursor.close()
    for rawitem in raw:
        hno = rawitem['hno']
        lcursor = connections['default'].cursor()
        lcursor.execute(
            "select lname from house,house_label where house.hno = house_label.hno and house_label.hno = %s",
            (hno,))
        rawitem['labels'] = dictfetchall(lcursor)
        lcursor.close()

        icursor = connections['default'].cursor()
        icursor.execute(
            "select pno,purl from house,house_pic where house.hno = house_pic.hno and house_pic.hno = %s",
            (hno,))
        rawitem['images'] = dictfetchall(icursor)
        icursor.close()
        if flag:
            delta_weidu = his_lati - float(rawitem['hlatitude'])
            delta_jingdu = his_longi - float(rawitem['hlongitude'])

            a = (delta_weidu * 3600) * 30.8
            b = (delta_jingdu * 3600) * 30.8 * math.cos(his_lati)
            c = math.sqrt(a * a + b * b)
            rawitem['c'] = c + 0.0
            if c < 1000:
                rawitem['distance'] = round(c)
                rawitem['danwei'] = 'm'
            else:
                rawitem['distance'] = round((c + 0.0) / 1000, 1)
                rawitem['danwei'] = 'km'

    #raw.sort(cmp=f2)
    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response


def index_location(request):

    flag = 0
    if request.GET['latitude'] and request.GET['longitude'] and request.GET['speed'] and request.GET['accuracy']:
        his_lati = float(request.GET['latitude'])
        his_longi = float(request.GET['longitude'])
        his_speed = request.GET['speed']
        his_accuracy = request.GET['accuracy']
        flag = 1

    openid = request.GET['openid']

    cursor = connections['default'].cursor()
    cursor.execute(
        "select house.hno,htitle1,htitle2,hprice,htype,hpic,hlongitude,hlatitude from house,house_display where house.hno = house_display.hno and house_display.hflag = 1 order by hprice ASC ")
    raw = dictfetchall(cursor)
    cursor.close()
    for rawitem in raw:
        hno = rawitem['hno']
        lcursor = connections['default'].cursor()
        lcursor.execute(
            "select lname from house,house_label where house.hno = house_label.hno and house_label.hno = %s",
            (hno,))
        rawitem['labels'] = dictfetchall(lcursor)
        lcursor.close()

        icursor = connections['default'].cursor()
        icursor.execute(
            "select pno,purl from house,house_pic where house.hno = house_pic.hno and house_pic.hno = %s",
            (hno,))
        rawitem['images'] = dictfetchall(icursor)
        icursor.close()
        if flag:
            delta_weidu = his_lati - float(rawitem['hlatitude'])
            delta_jingdu = his_longi - float(rawitem['hlongitude'])

            a = (delta_weidu * 3600) * 30.8
            b = (delta_jingdu * 3600) * 30.8 * math.cos(his_lati)
            c = math.sqrt(a*a + b*b)
            rawitem['c'] = c+0.0
            if c<1000:
                rawitem['distance'] = round(c)
                rawitem['danwei'] = 'm'
            else:
                rawitem['distance'] = round((c+0.0)/1000,1)
                rawitem['danwei'] = 'km'
    if flag:
        raw.sort(cmp = f2)
    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

