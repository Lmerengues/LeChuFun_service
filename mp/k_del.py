from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math
import os

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def del_activity(request):

    cursor = connections['klook'].cursor()
    cursor.execute("delete from activities where ano = %s",(request.GET['ano'],))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp