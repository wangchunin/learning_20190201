# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import AddForm




def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))
    )

def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    return  render(request, 'home.html', {'string': string})

def home1(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'home.html', {'TutorialList': TutorialList})

def home2(request):
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'home.html', {'info_dict': info_dict})

def home3(request):
    List = map(str, range(100))# 一个长度为100的 List
    return render(request, 'home.html', {'List': List})

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))


def index(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'index.html', {'form': form})


import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#from auto_reply.views import auto_reply_main  # 修改这里
from wechatpy import parse_message
from wechatpy.replies import TextReply

WEIXIN_TOKEN = 'wangchunin'


@csrf_exempt
def weixin_main(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        xml = request.body
        msg = parse_message(xml)
        print type(msg)
        request_meta = request.META
        info = []
        for k, v in request_meta.items():
            info.append(k)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

        print ip
        if msg.type == 'text':
            # 获取文本内容
            #content = msg.content
            content = unicode('王春林', 'utf-8')
            print msg.content
            print content,type(content)
            try:
                reply = TextReply(content=content, message=msg)
                r_xml = reply.render()
                # 获取唯一标记用户的openid，下文介绍获取用户信息会用到
                openid = msg.source
                print r_xml
                print type(r_xml)
                return HttpResponse(r_xml)
            except Exception as e:
                # 自行处理
                pass
        elif msg.type == 'event':
            try:
                push = ScanCodeWaitMsgEvent(msg)
                # 获取二维码信息，字符串
                content = msg.scan_result
                print content
                # 如何处理，自行处理，回复一段文本或者图文
                reply = TextReply(content="something", message=msg)
                r_xml = reply.render()
                return HttpResponse(r_xml)
            except Exception as e:
                # 暂时不处理
                pass

from wechatpy import WeChatClient

def create_menu(request):
    # 第一个参数是公众号里面的appID，第二个参数是appsecret
    client = WeChatClient("wxaa6be7392d75e2e9", "e9a5bd27d744f8421c315451eadbd29f")
    client.menu.create({
         "button": [
            {
                "type": "click",
                "name": "今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "type": "click",
                "name": "歌手简介",
                "key": "V1001_TODAY_SINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }
                ]
            }
            ],
         "matchrule": {
             "group_id": "2",
             "sex": "1",
             "country": "中国",
             "province": "广东",
             "city": "广州",
             "client_platform_type": "2"
        }
    })
    return HttpResponse('ok')
