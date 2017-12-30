from django.http import HttpResponse

import json
from django.db import connections

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

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


def index_price(request):
    cursor = connections['default'].cursor()
    cursor.execute(
        "select house.hno,htitle1,htitle2,hprice,htype,hpic from house,house_display where house.hno = house_display.hno and house_display.hflag = 1 order by hprice desc")
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