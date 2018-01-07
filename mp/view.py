# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
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
    context          = {}
    #context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def add(request):
    context          = {}
    #context['hello'] = 'Hello World!'


    cursor = connections['default'].cursor()
    cursor.execute("select * from equip")
    eraw = dictfetchall(cursor)
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select * from icon")
    iraw = dictfetchall(cursor)
    cursor.close()
    context['equips'] = eraw
    context['icons'] = iraw
    
    context['test'] = 'hello'

    return render(request, 'add.html', context)


def equips(request):
    cursor = connections['default'].cursor()
    cursor.execute("select * from equip")
    raw = dictfetchall(cursor)

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

def icons(request):
    cursor = connections['default'].cursor()
    cursor.execute("select * from icon")
    raw = dictfetchall(cursor)

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response


