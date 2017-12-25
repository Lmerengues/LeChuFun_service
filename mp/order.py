from django.http import HttpResponse

import json
from django.db import connections
from datetime import date, datetime
import pytz
tz  = pytz.timezone('Asia/Shanghai')
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
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
