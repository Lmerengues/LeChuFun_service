#!/usr/bin/python
# coding:utf-8
from django.http import HttpResponse
import urllib
import json
import hashlib
from django.db import connections
import logging
import random
import string
# import datetime
from datetime import date, datetime, time as time2
import time
import urllib2
import requests
# cursor = connections['default'].cursor()
import xml.etree.ElementTree as ET
# from flask import Flask, request, jsonify
# from datetime import date, datetime
import pytz
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date, time2)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


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


def create_sign(pay_data, merchant_key):
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    sign = hashlib.md5(stringSignTemp).hexdigest()
    return sign.upper()


def test(request):
    jucursor = connections['klook'].cursor()
    jucursor.execute("select bneed from Orders where oid = %s", ('1512391903',))
    raw = dictfetchall(jucursor)
    return HttpResponse(raw[0]['bneed'], 'text/html')


def index(request):
    # bno = request.GET['bno']
    # cursor.execute("select Orders.ono,ostatus,Seller.sno,sname,simg from Orders,Seller where Orders.sno = Seller.sno and Orders.bno = %s",(bno,))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_out_trade_no = str(int(time.time()))

    '''
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

    '''
    pno = request.GET['pno']
    total = request.GET['price_total']
    openid = request.GET['openid']
    date = request.GET['date']

    # then we start to do pay job
    data = {
        'appid': 'wx249ce8c7c0899bfc',
        'mch_id': '1338576301',
        'nonce_str': now,
        'body': 'aa-bb',
        'out_trade_no': my_out_trade_no,
        'total_fee': int(total)*100 ,
        'spbill_create_ip': '118.89.233.180',
        'notify_url': 'https://mina.mapglory.com/kpay_notify',
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
    # req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
    # result = urllib2.urlopen(req, timeout=10000).read()
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
    paySign = create_sign(paySign_data, 'n29sni59xnn593hdm3mpds8y3n386uop')
    paySign_data.pop('appId')
    paySign_data['paySign'] = paySign

    # after do all the pay job,we start to do order

    # resp = HttpResponse(json.dumps({'pp':prepay_id}), content_type="application/json")
    # return resp

    cursor = connections['klook'].cursor()
    cursor.execute("insert into orders values(null,%s,%s,%s,%s,%s,%s,sysdate(),%s,%s,%s,0)",
                   (my_out_trade_no, pno, openid, date, 'test', total, sign, paySign, prepay_id,))
    cursor.close()
    # then we judge if insert well
    jcursor = connections['klook'].cursor()
    jcursor.execute("select ono from orders where prepay_id = %s", (prepay_id,))
    data = {}
    paySign_data['my_status'] = 0
    if len(jcursor.fetchall()) >= 1:
        paySign_data['my_status'] = 1
        paySign_data['order_id'] = my_out_trade_no

    resp = HttpResponse(json.dumps(paySign_data), content_type="application/json")
    return resp


def send_order_mail(oid):
    tcursor = connections['klook'].cursor()
    tcursor.execute("select orders.oid,orders.hno,odate,ostart,oend,otype,onum,oready,obarbecue,"
                    "ofapiao,otip,ototal,orders.ocno,otime,htitle1,htitle2,uname,uphone,uwechat,ufirm,udepartment from orders,contact,house "
                    "where oid = %s and orders.ocno = contact.cno and orders.hno = house.hno", (oid,))

    raw = dictfetchall(tcursor)
    tcursor.close()

    my_type = ['聚会派对', '团建年会']
    my_num = ['1-5', '6-10', '11-20', '21-30']
    my_is = ['不需要', '提前一小时', '提前两小时', '提前三小时']

    str1 = '<p>订单号:' + raw[0]['oid'] + '</p>'
    str1 += '<p>场地名:' + raw[0]['htitle1'] + "·" + raw[0]['htitle2'] + '</p>'
    str1 += '<p>预约者姓名:' + raw[0]['uname'] + '</p>'
    str1 += '<p>预约者微信:' + raw[0]['uwechat'] + '</p>'
    str1 += '<p>预约者电话:' + raw[0]['uphone'] + '</p>'
    str1 += '<p>预约者公司/部门:' + raw[0]['ufirm'] + "/" + raw[0]['udepartment'] + '</p>'
    str1 += '<p>预约时间:' + json_serial(raw[0]['odate']) + "   " + json_serial(raw[0]['ostart']) + "-" + json_serial(
        raw[0]['oend']) + '</p>'
    str1 += '<p>下单金额:' + str(int(raw[0]['ototal']) / 100) + '</p>'
    str1 += '<p>下单时间:' + json_serial(raw[0]['otime']) + '</p>'
    str1 += '<p>预约类型:' + my_type[int(raw[0]['otype'])] + '</p>'
    str1 += '<p>预约人数:' + my_num[int(raw[0]['onum'])] + '</p>'
    str1 += '<p>是否需要准备:' + my_is[int(raw[0]['oready'])] + '</p>'
    str1 += '<p>是否需要烧烤设备:' + my_is[int(raw[0]['obarbecue'])] + '</p>'
    str1 += '<p>是否需要发票:' + my_is[int(raw[0]['ofapiao'])] + '</p>'
    str1 += '<p>附言:' + raw[0]['otip'] + '</p>'

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives('乐处Fun订单信息', str1, from_email,
                                 ['lechufun@163.com', 'liruishenshui@126.com'])

    msg.content_subtype = "html"
    msg.send()


def notify(request):
    tcursor = connections['klook'].cursor()
    tcursor.execute("insert into logs values(null,'test',sysdate())")
    tcursor.close()
    if request.method == 'POST':
        dict_data = xml_to_dict(request.body)

        jucursor = connections['klook'].cursor()
        jucursor.execute(
            "select oid,uno,ototal,otime,prepay_id,atitle1 from orders,activity_package,activities where oid = %s and activity_package.pno = orders.ano and activity_package.ano = activities.ano ",
            (dict_data['out_trade_no'],))
        raw = dictfetchall(jucursor)

        jucursor.close()

        # llcursor = connections['default'].cursor()
        # llcursor.execute("insert into logs values(null,%s,sysdate())",(dict_data['out_trade_no'],))
        # llcursor.close()


        if str(raw[0]['ototal']) != str(dict_data['total_fee']):
            # llcursor = connections['default'].cursor()
            # llcursor.execute("insert into logs values(null,%s,sysdate())",(str(jucursor)+'@'+str(dict_data['total_fee']),))
            # llcursor.close()
            return HttpResponse(
                "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",
                content_type="application/xml")


        llcursor = connections['klook'].cursor()
        llcursor.execute("insert into logs values(null,%s,sysdate())", ('hieheihei',))
        llcursor.close()

        ucursor = connections['klook'].cursor()
        ucursor.execute("update orders set ostatus = 1 where oid = %s", (dict_data['out_trade_no'],))

        if ucursor:
            llcursor = connections['klook'].cursor()
            llcursor.execute("insert into logs values(null,%s,sysdate())", ('hie2',))
            llcursor.close()

            url = "https://api.weixin.qq.com/cgi-bin/token"
            querystring = {"grant_type": "client_credential", "appid": "wx249ce8c7c0899bfc",
                           "secret": "e5e70d0f2e713a307c2beeb7f3eea8de"}
            headers = {}
            response = requests.request("GET", url, headers=headers, params=querystring)
            access_token = json.loads(response.text)['access_token']

            llcursor = connections['klook'].cursor()
            llcursor.execute("insert into logs values(null,%s,sysdate())", ('hie3',))
            llcursor.close()

            url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + access_token
            tmpdata = {"touser": raw[0]['uno'], "template_id": "2o5prNY_ljLX4tFt_9t2MDY2jI0xSpX3U9g3mkqF6iI",
                       "form_id": raw[0]['prepay_id'],
                       "data": {"keyword1": {"value": json_serial(raw[0]['otime']), "color": "#000000"},
                                "keyword2": {"value": dict_data['out_trade_no'], "color": "#000000"},
                                "keyword3": {"value": str(int(raw[0]['ototal']) / 100) + "元", "color": "#000000"},
                                "keyword4": {"value": raw[0]['atitle1'], "color": "#000000"}}}

            req = urllib2.Request(url, json.dumps(tmpdata), headers={'Content-Type': 'application/json'})
            result = urllib2.urlopen(req, timeout=30).read()

            # send_order_mail(dict_data['out_trade_no'])
            llcursor = connections['klook'].cursor()
            llcursor.execute("insert into logs values(null,%s,sysdate())",
                             ('errcode:-2' + result + "$" + str(tmpdata),))
            llcursor.close()
            #			result = str(result)
            llcursor = connections['klook'].cursor()
            llcursor.execute("insert into logs values(null,%s,sysdate())", ('errcode:-1',))
            llcursor.close()

        ucursor.close()

        return HttpResponse(
            "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>",
            content_type="application/xml")
