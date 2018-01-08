# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic

from django.db import connections

token = 'lmerengues'

cursor = connections['default'].cursor()

wechat = WechatBasic(token=token)


@csrf_exempt
def home(request):
    if wechat.check_signature(signature=request.GET['signature'],
                              timestamp=request.GET['timestamp'],
                              nonce=request.GET['nonce']):
        if request.method == 'GET':
            rsp = request.GET.get('echostr', 'error')
        else:
            wechat.parse_data(request.body)
            inputs = wechat.message.content
            # rsp = wechat.response_text(message)
            # return HttpResponse(rsp)

            inputs = inputs.split()
            judge_str = inputs[0].lower()
            if (len(inputs) > 1 and (judge_str == "身高" or judge_str == "h")):
                data_str = inputs[1].lower()
                if (data_str == "n" and len(inputs) > 2):
                    return lookupPE_height(inputs[2], 2)
                return lookupPE_height(data_str, 1)
            elif (len(inputs) > 1 and (judge_str == "体重" or judge_str == "w")):
                data_str = inputs[1].lower()
                if (data_str == "n" and len(inputs) > 2):
                    return lookupPE_weight(inputs[2], 2)
                return lookupPE_weight(data_str, 1)
            elif (len(inputs) > 1 and (judge_str == "pe")):
                data_str = inputs[1].lower()
                if (data_str == "n" and len(inputs) > 2):
                    return lookupPE_pe(inputs[2], 2)
                return lookupPE_pe(data_str, 1)
            else:
                return HttpResponse(wechat.response_text("该功能尚未开放哟,或许你是输错了呢,试试输入“学号两个字+空格+2015201984”来体验学号查询吧~"))
    else:
        rsp = wechat.response_text('check error')


def lookupPE_height(sno, mode):
    pecursor = connections['rucpe'].cursor()
    if (sno == '2015201984' or sno == "马正一"):
        return HttpResponse(wechat.response_news([{'title': "无可奉告", 'description': '告辞'}]))
    if mode == 1:
        pecursor.execute(
            "select * from pe_grade,pe_student where pe_grade.sno = pe_student.sno and pe_grade.sno  = %s and tno = 4",
            [sno])
    else:
        pecursor.execute(
            "select * from pe_grade,pe_student where pe_grade.sno = pe_student.sno and pe_student.sname  = %s and tno = 4",
            [sno])
    raw = pecursor.fetchall()
    if (len(raw) == 1):
        resultstr = '身高:' + str(raw[0][1]) + "cm"
        sname = raw[0][6]
        return HttpResponse(wechat.response_news([{'title': sname + "的身高", 'description': resultstr}]))
    elif len(raw) > 1 and mode != 1:
        return HttpResponse(wechat.response_text("重名了！"))
    else:
        resultstr = '太笨了没查到哎'
        return HttpResponse(wechat.response_text(resultstr))


def lookupPE_weight(sno, mode):
    pecursor = connections['rucpe'].cursor()
    if (sno == '2015201984' or sno == "马正一"):
        return HttpResponse(wechat.response_news([{'title': "无可奉告", 'description': '告辞'}]))
    if mode == 1:
        pecursor.execute(
            "select * from pe_grade,pe_student where pe_grade.sno = pe_student.sno and pe_grade.sno  = %s and tno = 5",
            [sno])
    else:
        pecursor.execute(
            "select * from pe_grade,pe_student where pe_grade.sno = pe_student.sno and pe_student.sname  = %s and tno = 5",
            [sno])
    raw = pecursor.fetchall()
    if (len(raw) == 1):
        resultstr = '体重:' + str(raw[0][1]) + "kg"
        sname = raw[0][6]
        return HttpResponse(wechat.response_news([{'title': sname + "的体重", 'description': resultstr}]))
    elif len(raw) > 1 and mode != 1:
        return HttpResponse(wechat.response_text("重名了！"))
    else:
        resultstr = '太笨了没查到哎'
        return HttpResponse(wechat.response_text(resultstr))


def lookupPE_pe(sno, mode):
    pecursor = connections['rucpe'].cursor()
    if (sno == '2015201984' or sno == "马正一"):
        return HttpResponse(wechat.response_news([{'title': "无可奉告", 'description': '告辞'}]))
    if mode == 1:
        pecursor.execute(
            "select pe_grade.sno,pe_grade.sgrade,sscore,srate,pe_type.tno,tname,tdimen,sname from pe_grade,pe_student,pe_type where pe_grade.sno = pe_student.sno and pe_grade.sno  = %s and pe_grade.tno = pe_type.tno",
            [sno])
    else:

        pecursor.execute("select * from pe_student where sname = %s", [sno])
        praw = pecursor.fetchall()
        if (len(praw) > 1):
            return HttpResponse(wechat.response_text("重名了！"))
        pecursor.execute(
            "select pe_grade.sno,pe_grade.sgrade,sscore,srate,pe_type.tno,tname,tdimen,sname from pe_grade,pe_student,pe_type where pe_grade.sno = pe_student.sno and pe_student.sname  = %s and pe_grade.tno = pe_type.tno",
            [sno])
    raw = pecursor.fetchall()
    if (len(raw) > 0):
        # resultstr = '体重:'+str(raw[0][1])+"kg"
        # sname = raw[0][6]
        resultstr = ''
        for hitem in raw:
            # resultstr += "课程:" + hitem[0] + "\n" + "课程号:" + str(hitem[1]) + "\n" + "作业名:" + hitem[2] + "\n" + "布置时间:" + str(hitem[4]) + "\n" + "截止时间:" + str(hitem[5]) + "\n" + "------" + "\n"
            # return HttpResponse(wechat.response_news([{'title':sname+"的体重",'description':resultstr}]))
            resultstr += '项目:' + hitem[5] + "\n成绩:" + str(hitem[1]) + hitem[6] + "\n分数:" + str(hitem[2]) + "\n等级:" + \
                         hitem[3] + "\n------------------------------\n"
        return HttpResponse(wechat.response_news([{'title': raw[0][7] + "的体测成绩", 'description': resultstr}]))
    else:
        resultstr = '太笨了没查到哎'
        return HttpResponse(wechat.response_text(resultstr))