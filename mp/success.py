from django.http import HttpResponse

import json
from django.db import connections


# cursor = connections['default'].cursor()

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def index(request):
    hno = request.GET['hno']
    cno = request.GET['cno']

    cursor = connections['default'].cursor()
    cursor.execute("select * from house where house.hno = %s", (hno,))
    raw = dictfetchall(cursor)
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select uname,uphone,uwechat from contact where cno = %s", (cno,))
    craw = dictfetchall(cursor)
    cursor.close()



    lcursor = connections['default'].cursor()
    lcursor.execute("select lno,lname from house_label where hno = %s", (hno,))
    raw[0]['labels'] = dictfetchall(lcursor)
    lcursor.close()

    pcursor = connections['default'].cursor()
    pcursor.execute("select pno,purl from house_pic where hno = %s", (hno,))
    raw[0]['images'] = dictfetchall(pcursor)
    pcursor.close()

    icursor = connections['default'].cursor()
    icursor.execute(
        "select iname,iurl from icon,house_icon where house_icon.ino = icon.ino and house_icon.hno = %s", (hno,))
    raw[0]['icons'] = dictfetchall(icursor)
    lcursor.close()

    mcursor = connections['default'].cursor()
    mcursor.execute(
        "select murl from house_memory where hno = %s", (hno,))
    raw[0]['memory'] = dictfetchall(mcursor)
    mcursor.close()

    equips = {}
    ecursor = connections['default'].cursor()
    ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s and "
                    "equip.eno = house_equip.eno and tno = 1", (hno,))
    equips['videos'] = dictfetchall(ecursor)
    ecursor = connections['default'].cursor()
    ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s "
                    "and equip.eno = house_equip.eno and tno = 2", (hno,))
    equips['game'] = dictfetchall(ecursor)
    ecursor = connections['default'].cursor()
    ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s "
                    "and equip.eno = house_equip.eno and tno = 3", (hno,))
    equips['meal'] = dictfetchall(ecursor)
    ecursor.close()

    raw[0]['equip'] = equips
    response = HttpResponse(json.dumps([raw,craw]), content_type="application/json")
    return response

