#!/usr/bin/python
#coding:utf-8
from django.http import HttpResponse
import urllib
import json
import hashlib
from django.db import connections
import logging
import random
import string
#import datetime
from datetime import date, datetime
import time
import urllib2
import requests
#cursor = connections['default'].cursor()
import xml.etree.ElementTree as ET
#from flask import Flask, request, jsonify
#from datetime import date, datetime
import pytz
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]
def dict_to_xml(dict_data):
    '''
    dict to xml
    :param dict_data:
    :return:
    '''
    xml = ["<xml>"]
    for k, v in dict_data.iteritems():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)

def xml_to_dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict

def create_sign(pay_data,merchant_key):
        
	stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
        sign = hashlib.md5(stringSignTemp).hexdigest()
        return sign.upper()
def test(request):
        jucursor = connections['default'].cursor()
        jucursor.execute("select bneed from Orders where oid = %s",('1512391903',))
	raw = dictfetchall(jucursor)
        return HttpResponse(raw[0]['bneed'],'text/html')


def index(request):

	#bno = request.GET['bno']
	#cursor.execute("select Orders.ono,ostatus,Seller.sno,sname,simg from Orders,Seller where Orders.sno = Seller.sno and Orders.bno = %s",(bno,))
	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	my_out_trade_no = str(int(time.time()))

	hno = request.GET['hno']
	date = request.GET['date']
	time_start = request.GET['start'] + ":00"
	time_end = request.GET['end'] + ":00"
	type = request.GET['type']
	ready = request.GET['ready']
	num = request.GET['num']
	barb = request.GET['barb']
	fapiao = request.GET['fapiao']
	tip = request.GET['tip']
	total = request.GET['price_total']
	openid = request.GET['openid']
	cno = request.GET['cno']

# then we start to do pay job
	data = {
        	'appid': 'wx08912a543bda29bc',
         	'mch_id': '1338576301',
        	'nonce_str': now,
       	 	'body': 'aa-bb',
        	'out_trade_no': my_out_trade_no,
       	 	'total_fee': int(total)*100,
        	'spbill_create_ip': '118.89.233.180',
        	'notify_url': 'https://mina.mapglory.com/pay_notify',
        	'attach': '{"msg": "test"}',
        	'trade_type': 'JSAPI',
     	  	'openid': openid
   	 }
	stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
	stringSignTemp = '{0}&key={1}'.format(stringA, "n29sni59xnn593hdm3mpds8y3n386uop")
	sign = hashlib.md5(stringSignTemp).hexdigest().upper()

	data['sign'] = sign
	data = dict_to_xml(data)
	url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
	#req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
    	 #result = urllib2.urlopen(req, timeout=10000).read()
#    	 headers = {
#	'Content-Type': 'application/xml',
 #   		}
#
 #   	 response = requests.request("POST", url, headers=headers, params=data)
	req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
	result = urllib2.urlopen(req, timeout=30).read()
	prepay_id = xml_to_dict(result).get('prepay_id')
	paySign_data = {
                'appId': 'wx08912a543bda29bc',
                'timeStamp': my_out_trade_no,
                'nonceStr': now,
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD5',
            }
	paySign = create_sign(paySign_data,'n29sni59xnn593hdm3mpds8y3n386uop')
	paySign_data.pop('appId')
	paySign_data['paySign'] = paySign
	 
# after do all the pay job,we start to do order

	resp = HttpResponse(json.dumps({'pp':prepay_id}), content_type="application/json")
	return resp

	cursor = connections['default'].cursor()
	cursor.execute("insert into orders values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,sysdate(),%s,%s,%s,'0')",
				   (my_out_trade_no,hno,openid,date,time_start,time_end,type,num,ready,
					barb,fapiao,tip,str(int(total)*100),cno,sign,paySign,prepay_id,))
	cursor.close()
# then we judge if insert well
	jcursor = connections['default'].cursor()
	jcursor.execute("select ono from orders where prepay_id = %s",(prepay_id,))
	data = {}
	paySign_data['my_status'] = 0
	if len(jcursor.fetchall()) >= 1:
		paySign_data['my_status'] = 1
		paySign_data['order_id'] = my_out_trade_no

	resp = HttpResponse(json.dumps(paySign_data), content_type="application/json")
	return resp

def notify(request):

	tcursor = connections['default'].cursor()
	tcursor.execute("insert into logs values(null,'test',sysdate())")
	tcursor.close()
	if request.method == 'POST':
		dict_data = xml_to_dict(request.body)


		jucursor = connections['default'].cursor()
		jucursor.execute("select oid,uno,ototal,otime,prepay_id from Orders where oid = %s ",(dict_data['out_trade_no'],))
		raw = dictfetchall(jucursor)

		jucursor.close()

		#llcursor = connections['default'].cursor()
                #llcursor.execute("insert into logs values(null,%s,sysdate())",(dict_data['out_trade_no'],))
                #llcursor.close()

		if str(raw[0]['ototal']) != str(dict_data['total_fee']):
			#llcursor = connections['default'].cursor()
			#llcursor.execute("insert into logs values(null,%s,sysdate())",(str(jucursor)+'@'+str(dict_data['total_fee']),))
			#llcursor.close()
			return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",content_type="application/xml")
		
		llcursor = connections['default'].cursor()
		llcursor.execute("insert into logs values(null,%s,sysdate())",('hieheihei',))
		llcursor.close()


		ucursor = connections['default'].cursor()
		ucursor.execute("update Orders set ostatus = 1 where oid = %s",(dict_data['out_trade_no'],))

		if ucursor:
			llcursor = connections['default'].cursor()
			llcursor.execute("insert into logs values(null,%s,sysdate())",('hie2',))
			llcursor.close()

			url = "https://api.weixin.qq.com/cgi-bin/token"
			querystring = {"grant_type":"client_credential","appid":"wx08912a543bda29bc","secret":"0b0d2c8666c0504d696c5cddd342ba17"}
			headers = {}
			response = requests.request("GET", url, headers=headers, params=querystring)
			access_token = json.loads(response.text)['access_token']

			llcursor = connections['default'].cursor()
			llcursor.execute("insert into logs values(null,%s,sysdate())",('hie3',))
			llcursor.close()

			url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token="+access_token
			tmpdata={"touser":raw[0]['uno'],"template_id":"r2-xlRvYeETDndxslsDy44ReOf01wV5xVOjYZCT8Rw8","form_id":raw[0]['prepay_id'],"data":{"keyword1": {"value": json_serial(raw[0]['otime']), "color": "#000000"}, "keyword2": {"value": dict_data['out_trade_no'], "color": "#000000"}, "keyword3": {"value": str(int(raw[0]['ototal'])/100)+"元", "color": "#000000"} , "keyword4": {"value": "test", "color": "#000000"}}}

			req = urllib2.Request(url, json.dumps(tmpdata), headers={'Content-Type': 'application/json'})
			result = urllib2.urlopen(req, timeout=30).read()
			llcursor = connections['default'].cursor()
			llcursor.execute("insert into logs values(null,%s,sysdate())",('errcode:-2'+result+"$"+str(tmpdata),))
			llcursor.close()
#			result = str(result)
			llcursor = connections['default'].cursor()
			llcursor.execute("insert into logs values(null,%s,sysdate())",('errcode:-1',))
			llcursor.close()

		ucursor.close()

		return HttpResponse("<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",content_type="application/xml")
