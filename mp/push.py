from django.http import HttpResponse

import json
from django.db import connections

import math
import hashlib

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

    signature = request.GET["signature"]
    timestamp = request.GET["timestamp"]
    nonce = request.GET["nonce"]

    token = 'lechufun2017'

    arr = [token,timestamp,nonce]
    array = sorted(arr)
    str = array[0]+array[1]+array[2]
    str = hashlib.sha1(str).hexdigest()
    if str == signature:
        return HttpResponse(request.GET['echostr'], content_type="application/json")
    else:
        return HttpResponse('?', content_type="application/json")

'''

def index(request):

    tcursor = connections['default'].cursor()
    tcursor.execute("insert into logs values(null,'kefu',sysdate())")
    tcursor.close()
    return HttpResponse('success', content_type="application/json")




