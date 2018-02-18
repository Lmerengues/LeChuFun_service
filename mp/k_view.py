# -*- coding: utf-8 -*-

# from django.http import HttpResponse
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
    context = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)


def add(request):
    context = {}
    # context['hello'] = 'Hello World!'


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

    cursor = connections['klook'].cursor()
    cursor.execute("select pno,ptitle from place")
    praw = dictfetchall(cursor)
    cursor.close()
    context['places'] = praw

    # context['test'] = 'hello'


    return render(request, 'k_add.html', context)


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


def addHouseHandle(request):
    rb = request.POST['htitle1']
    cursor = connections['default'].cursor()
    cursor.execute("insert into logs values(null,%s,sysdate())", (rb,))
    cursor.close()

    raw = {'status': 1}
    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response


def activity_list(request):
    context = {}
    # context['hello'] = 'Hello World!'


    cursor = connections['klook'].cursor()
    cursor.execute("select ano,atitle1 from activities")
    eraw = dictfetchall(cursor)
    cursor.close()

    for item in eraw:
        cursor = connections['klook'].cursor()
        cursor.execute("select aval from activity_rank_hot where ano = %s",(item['ano'],))
        item['hval'] =  dictfetchall(cursor)[0]['aval']
        cursor.close()

        cursor = connections['klook'].cursor()
        cursor.execute("select aval from activity_rank_theme where ano = %s", (item['ano'],))
        item['tval'] = dictfetchall(cursor)[0]['aval']
        cursor.close()

        cursor = connections['klook'].cursor()
        cursor.execute("select aval from activity_rank_recommend where ano = %s", (item['ano'],))
        item['rval'] = dictfetchall(cursor)[0]['aval']
        cursor.close()

    context['list'] = eraw


    # context['test'] = 'hello'


    return render(request, 'k_activity.html', context)

def activity_rule(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'k_rule.html', context)

def activity_instruction(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'k_instruction.html', context)

def activity_use(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'k_use.html', context)

def activity_refund(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'k_refund.html', context)

def activity_image(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'k_image.html', context)

def activity_package(request):
    context = {}
    # context['hello'] = 'Hello World!'

    ano = request.GET['ano']

    cursor = connections['klook'].cursor()
    cursor.execute("select pno,ptitle from activity_package where ano = %s",(ano,))
    eraw = dictfetchall(cursor)
    cursor.close()

    context['list'] = eraw



    return render(request, 'k_package.html', context)

def package_rule(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'p_rule.html', context)

def package_ticket(request):
    context = {}
    # context['hello'] = 'Hello World!'


    return render(request, 'p_ticket.html', context)

def city_add(request):
    context = {}

    return render(request, 'k_cityadd.html', context)