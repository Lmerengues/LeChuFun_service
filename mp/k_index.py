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


def index(request):

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select pno,ptitle,purl from place,place_hot where place.pno = place_hot.pno order by pval desc")
    raw = dictfetchall(cursor)
    cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

