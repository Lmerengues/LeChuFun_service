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
	cursor = connections['default'].cursor()	    
    #return HttpResponse("Hello world ! ")
	sno = request.GET['sno']
	cursor.execute("select Seller.sno,sname,swage from Seller where Seller.sno = %s",(sno,))
	raw = dictfetchall(cursor)
	cursor.close()
	
	response = HttpResponse(json.dumps(raw),content_type="application/json")	
	return response

def submit(request):
   	hour = request.GET['hour']
    	need = request.GET['need']
    	sno = request.GET['sno']
    	bno = request.GET['bno']
	note = request.GET['note']
    	#bno = 7
	scursor = connections['default'].cursor()
	scursor.execute("select ono from Orders where bno = %s and sno = %s",(bno,sno))
	if(len(scursor.fetchall())>0):
		data = {}
		data['status'] = 2
		response = HttpResponse(json.dumps(data),content_type="application/json")
        	return response
		
	
    	cursor = connections['default'].cursor()
    	cursor.execute("insert into Orders values(null,%s,%s,%s,%s,%s,sysdate(),0)",(bno,sno,hour,need,note,))
    	cursor.close()

    	jcursor = connections['default'].cursor()
    	jcursor.execute("select ono from Orders where bno = %s and sno = %s",(bno,sno,))
   	data = {}
    	data['status'] = 0
    	if len(jcursor.fetchall()) >= 1:
        	data['status'] = 1
    	response = HttpResponse(json.dumps(data),content_type="application/json")
   	return response	


