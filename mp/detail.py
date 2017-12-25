from django.http import HttpResponse

import json
from django.db import connections

#cursor = connections['default'].cursor()

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]
def index(request):

	hno = request.GET['hno']

	cursor = connections['default'].cursor()
	cursor.execute("select * from house where house.hno = %s",(hno,))
	raw = dictfetchall(cursor)
	cursor.close()

	lcursor = connections['default'].cursor()
	lcursor.execute("select lno,lname from house_label where hno = %s",(hno,))
	raw[0]['labels'] = dictfetchall(lcursor)
	lcursor.close()

	pcursor = connections['default'].cursor()
	pcursor.execute("select pno,purl from house_pic where hno = %s",(hno,))
	raw[0]['images'] = dictfetchall(pcursor)
	pcursor.close()

	icursor = connections['default'].cursor()
	icursor.execute(
		"select iname,iurl from icon,house_icon where house_icon.ino = icon.ino and house_icon.hno = %s", (hno,))
	raw[0]['icons'] = dictfetchall(lcursor)
	lcursor.close()

	mcursor = connections['default'].cursor()
	mcursor.execute(
		"select murl from house_memory where hno = %s", (hno,))
	raw[0]['memory'] = dictfetchall(lcursor)
	mcursor.close()

	equips = {}
	ecursor = connections['default'].cursor()
	ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s and "
					"equip.eno = house_equip.eno and tno = 1", (hno,))
	equips['videos'] = dictfetchall(pcursor)
	ecursor = connections['default'].cursor()
	ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s "
		"and equip.eno = house_equip.eno and tno = 2",(hno,))
	equips['game'] = dictfetchall(pcursor)
	ecursor = connections['default'].cursor()
	ecursor.execute("select eurl,ename from house_equip,equip where house_equip.hno = %s "
		"and equip.eno = house_equip.eno and tno = 3",(hno,))
	equips['meal'] = dictfetchall(pcursor)
	ecursor.close()

	raw[0]['equip'] = equips
	response = HttpResponse(json.dumps(raw),content_type="application/json")	
	return response


def like(request):
	scursor = connections['default'].cursor()
	scursor.execute("select * from Seller_like where sno = %s and bno = %s",(request.GET['sno'],request.GET['bno'],))
	raw = dictfetchall(scursor)
	data = {}
	if(len(raw)>0):
		data['status'] = 2
		response = HttpResponse(json.dumps(data),content_type="application/json")
		return response
	
	lcursor = connections['default'].cursor()
	flag1 = lcursor.execute("insert into Seller_like values(%s,%s)",(request.GET['bno'],request.GET['sno'],))
	if flag1:
		ucursor = connections['default'].cursor()
		flag2 = ucursor.execute("update Seller set slike = slike + 1 where Seller.sno = %s",(request.GET['sno'],))
		if flag2:
			data['status'] = 1
			response = HttpResponse(json.dumps(data),content_type="application/json")
			return response
	data['status'] = 0
	response = HttpResponse(json.dumps(data),content_type="application/json")
	return response
