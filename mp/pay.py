from django.http import HttpResponse

import json
import hashlib
from django.db import connections
import logging
import random
import string
import datetime
import time
import urllib2
import requests
#cursor = connections['default'].cursor()
import xml.etree.ElementTree as ET
#from flask import Flask, request, jsonify


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
	#cursor = connections['default'].cursor()	    
    #return HttpResponse("Hello world ! ")
	 bno = request.GET['bno']
	#cursor.execute("select Orders.ono,ostatus,Seller.sno,sname,simg from Orders,Seller where Orders.sno = Seller.sno and Orders.bno = %s",(bno,))
         now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         my_out_trade_no = str(int(time.time()))

	 hour = request.GET['hour']
         need = request.GET['need']
         sno = request.GET['sno']
         note = request.GET['note']
#first we should know if he had orderd the same girl before
	 scursor = connections['default'].cursor()
         scursor.execute("select ono from Orders where bno = %s and sno = %s and ostatus = 1",(bno,sno))
         if(len(scursor.fetchall())>0):
         	data = {}
                data['my_status'] = 2
                response = HttpResponse(json.dumps(data),content_type="application/json")
                return response	 
# then we start to do pay job	 
	 data = {
        	'appid': 'wx249ce8c7c0899bfc',
         	'mch_id': '1338576301',
        	'nonce_str': now,
       	 	'body': 'aa-bb',
        	'out_trade_no': my_out_trade_no,
       	 	'total_fee': need,
        	'spbill_create_ip': '118.89.233.180',
        	'notify_url': 'https://mina.mapglory.com/pay_notify',
        	'attach': '{"msg": "test"}',
        	'trade_type': 'JSAPI',
     	  	'openid': bno
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
                'appId': 'wx249ce8c7c0899bfc',
                'timeStamp': my_out_trade_no,
                'nonceStr': now,
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD5',
            }
	 paySign = create_sign(paySign_data,'n29sni59xnn593hdm3mpds8y3n386uop')
	 paySign_data.pop('appId')
	 paySign_data['paySign'] = paySign 
	 
# after do all the pay job,we start to do order
	 cursor = connections['default'].cursor()
         cursor.execute("insert into Orders values(null,%s,%s,%s,%s,%s,%s,sysdate(),0,%s,%s)",(my_out_trade_no,bno,sno,hour,need,note,sign,paySign,))
         cursor.close()
# then we judge if insert well	 
	 jcursor = connections['default'].cursor()
         jcursor.execute("select ono from Orders where bno = %s and sno = %s",(bno,sno,))
         data = {}
         paySign_data['my_status'] = 0
         if len(jcursor.fetchall()) >= 1:
         	paySign_data['my_status'] = 1
		paySign_data['order_id'] = my_out_trade_no
	 
    	 resp = HttpResponse(json.dumps(paySign_data), content_type="application/json")
    	 return resp

def notify(request):

    	# data= {}
    	# data['status'] = 1
    	# response = HttpResponse(json.dumps(data), content_type="application/json")
    	# return response
	tcursor = connections['default'].cursor()
	tcursor.execute("insert into logs values(null,'test',sysdate())")
        tcursor.close()	
#	rstr = str(request)
#	file_object = open('/static/thefile.txt', 'w')
#	file_object.write("b")
#	file_object.close( )
	if request.method == 'POST':
		dict_data = xml_to_dict(request.body)
        	#logging.info(dict_data)
		#cursor = connections['default'].cursor()
		#cursor.execute("insert into logs values(null,%s,sysdate())",(dict_data['appid'],))
		#cursor.close()
	
		
        	#stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
         	#stringSignTemp = '{0}&key={1}'.format(stringA, "n29sni59xnn593hdm3mpds8y3n386uop")
         #	sign = "121212"
	#	if sign != dict_data['sign']:
	#		llcursor = connections['default'].cursor()
         #       	llcursor.execute("insert into logs values(null,%s,sysdate())",(sign+'@'+dict_data['sign']+'@'+dict_data['out_trade_no'],))
          #      	llcursor.close()
	#		return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",content_type="application/xml")
        	jucursor = connections['default'].cursor()
		jucursor.execute("select bneed from Orders where oid = %s",(dict_data['out_trade_no'],))
		raw = dictfetchall(jucursor)

		jucursor.close()
		
		#llcursor = connections['default'].cursor()
                #llcursor.execute("insert into logs values(null,%s,sysdate())",(dict_data['out_trade_no'],))
                #llcursor.close()
		
		if str(raw[0]['bneed']) != str(dict_data['total_fee']):
			llcursor = connections['default'].cursor()
         	        llcursor.execute("insert into logs values(null,%s,sysdate())",(str(jucursor)+'@'+str(dict_data['total_fee']),))
          		llcursor.close()
        		return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",content_type="application/xml")
		
		llcursor = connections['default'].cursor()
                llcursor.execute("insert into logs values(null,%s,sysdate())",('hieheihei',))
		llcursor.close()
		ucursor = connections['default'].cursor()
        	ucursor.execute("update Orders set ostatus = 1 where oid = %s",(dict_data['out_trade_no'],))
        	ucursor.close()
	
        	return HttpResponse("<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",content_type="application/xml")