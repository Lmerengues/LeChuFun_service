from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math

def add_activity(request):

    cursor = connections['klook'].cursor()
    cursor.execute("insert into base values(null,%s,%s)",('a','b',))
    cursor.close()

    raw = {'status':1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp