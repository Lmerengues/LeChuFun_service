from django.http import HttpResponse

import json
from django.db import connections
from datetime import date, datetime,time
import pytz
tz  = pytz.timezone('Asia/Shanghai')
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date,time)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

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
	cursor.execute("select hno,htitle1,htitle2,htitle3,hpic from house where house.hno = %s",(hno,))
	raw = dictfetchall(cursor)
	cursor.close()

	response = HttpResponse(json.dumps(raw),content_type="application/json")	
	return response

def time_split(timestr):

	arr = timestr.split(':')
	hour = int(arr[0])
	min = int(arr[1])

	min_chuo = hour*60+min
	return min_chuo

def cal_price(request):
	hno = request.GET['hno']


	time_start = request.GET['timestart']
	time_end = request.GET['timeend']

	mins = time_split(time_end) - time_split(time_start)
	hours = round((mins+0.0)/60)

	cursor = connections['default'].cursor()
	cursor.execute("select hprice from house where house.hno = %s", (hno,))
	raw = dictfetchall(cursor)
	price_per_hour = raw[0]['hprice']
	cursor.close()

	price_total = price_per_hour * hours
	response = HttpResponse(json.dumps({"total_price":price_total}), content_type="application/json")
	return response


def check_date(request):

	hno = request.GET['hno']
	date = request.GET['date']

	cursor = connections['default'].cursor()
	cursor.execute("select ostart,oend from orders where hno = %s and odate = %s and ostatus = 1", (hno,date,))
	time_dict = dictfetchall(cursor)

	for item in time_dict:
		item['ostart']  = json_serial(item['ostart'])
		item['oend'] = json_serial(item['oend'])


	dict = {"times":time_dict}
	if len(time_dict) == 0:
		dict['status'] = 0
	else:
		dict['status'] = 1


	response = HttpResponse(json.dumps(time_dict), content_type="application/json")
	return response
















