# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse

import json
from django.db import connections
import datetime

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def date_pro(date_str):         #2017-02-03日期字符串解析
    arr = date_str.split('-')
    year = int(arr[0])
    month = int(arr[1])
    day = int(arr[2])
    return {'year':year,'month':month,'day':day,'arr':arr}

def index(request):

    hno = request.GET['hno']
    time_start = request.GET['timestart']
    time_end = request.GET['timeend']
    date = request.GET['date']
    num = request.GET['num']

    mins = time_split(time_end) - time_split(time_start)
    hours = round((mins + 0.0) / 60)

    cursor = connections['default'].cursor()
    cursor.execute("select htitle1,hpic,hprice from house where house.hno = %s",(hno,))
    house_raw = dictfetchall(cursor)
    price_per_hour = house_raw[0]['hprice']
    cursor.close()


    mydate = date_pro(date)
    anyday = datetime.datetime(mydate['year'], mydate['month'], mydate['day']).strftime("%w")
    week_str_arr = ['日','一','二','三','四','五','六']
    date_total_str = mydate['arr'][0]+"年"+mydate['arr'][1]+"月"+mydate['arr'][2]+"日星期"+week_str_arr[anyday]

    time_total_str = time_start+"至"+time_end

    price_detail = []
    price_total = price_per_hour * hours
    item = {"name":"空间信息","price":"￥"+str(price_total)}
    price_detail.append(item)

    cursor = connections['default'].cursor()
    cursor.execute("select * from house_discount where house.hno = %s order by hour desc", (hno,))
    house_dis = dictfetchall(cursor)
    if(len(house_dis)!= 0):
        item = {"name":"满"+str(house_dis[0]['hour'])+"小时减"+str(house_dis[0]['discount']),
                "price":"-￥"+str(house_dis[0]['discount'])}
        price_detail.append(item)
        price_total -= int(house_dis[0]['discount'])

    num_arr = [5,10,20,30]
    price_ave = price_total/num_arr[int(num)]

    dict = {'house_info':house_raw,'date':date_total_str,'time':time_total_str,'detail':price_detail,
            'price_total':price_total,'price_ave':price_ave}

    response = HttpResponse(json.dumps(dict),content_type="application/json")
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
















