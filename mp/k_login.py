from django.http import HttpResponse

import json
from django.db import connections

import requests


# cursor = connections['default'].cursor()

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def login(res):
    url = "https://api.weixin.qq.com/sns/jscode2session"

    querystring = {"appid": "wx249ce8c7c0899bfc", "secret": "fd8e74092472b06caeaf209bab00bf80",
                   "js_code": res.GET['code'], "grant_type": "authorization_code"}

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        'x-devtools-emulate-network-conditions-client-id': "6d9ff6c0-092e-41e9-970a-169d453074a6",
        'upgrade-insecure-requests': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    userdata = json.loads(response.text)
    cursor = connections['klook'].cursor()

    #resp = HttpResponse(json.dumps(userdata), content_type="application/json")

    #return resp

    cursor.execute("select * from Users where uid = %s", (userdata['openid'],))

    flag = 1
    if (len(cursor.fetchall()) == 0):


        rawdata = json.loads(res.GET['rawData'])
        icursor = connections['klook'].cursor()
        #resp = HttpResponse(json.dumps(userdata), content_type="application/json")

        #return resp
        icursor.execute("insert into Users values(%s,%s,%s,%s,%s,%s,%s,%s,sysdate(),0)", (userdata['openid'], rawdata['nickName'], rawdata['gender'], rawdata['language'], rawdata['city'],rawdata['province'], rawdata['country'], rawdata['avatarUrl'],))

        icursor.close()

    cursor.close()

    loginret = {}
    loginret['openid'] = userdata['openid']

    resp = HttpResponse(json.dumps(loginret), content_type="application/json")

    return resp
