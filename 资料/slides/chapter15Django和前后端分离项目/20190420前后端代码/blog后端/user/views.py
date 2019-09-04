from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

# Create your views here.
import simplejson
from .models import User
import bcrypt
import jwt
from django.conf import settings
import datetime

AUTH_EXPIRE = 8 * 60 * 60

def gen_token(user_id):
    print(settings.ALG)
    return  jwt.encode({
            'user_id': user_id,
            #'timestamp': int(datetime.datetime.now().timestamp()),
            'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
        }, settings.SECRET_KEY, settings.ALG).decode()


def reg(request:HttpRequest):

    try:
        payload = simplejson.loads(request.body)
        print(payload, type(payload))
        email = payload['email']

        user = User.objects.filter(email=email)
        print(user.query)
        print(user, type(user))
        if user.first(): # 代表有数据
            print('~~~~~~~~~~~~~~')
            return HttpResponseBadRequest()

        # 没有此邮箱
        name = payload['name']
        password = payload['password']
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(email, name, password)

        user = User()
        user.name = name
        user.email = email
        user.password = password


        user.save() # 保持数据，django的model save、delete会自动提交

        return JsonResponse({
                'user':{
                    'user_id':user.id,
                    'name':user.name,
                    'email':user.email,
                }, 'token':gen_token(user.id)
            }, status=201) # created

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()



def login(request:HttpRequest):
    # post json

    try:
        payload = simplejson.loads(request.body)
        email = payload['email']

        user = User.objects.get(email=email) # only one

        # 验证密码
        if bcrypt.checkpw(payload['password'].encode(), user.password.encode()):
            token = gen_token(user.id)
            res = JsonResponse({
                'user':{
                    'user_id':user.id,
                    'name':user.name,
                    'email':user.email,
                }, 'token':token
            })
            res.set_cookie('jwt', token)
            return res
        else:
            return HttpResponseBadRequest()

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


# 所有请求都做认证
class SimpleMiddleware(object):
    address = {}  # 以后在这里直接访问第三方存储服务，例如Redis，kv nosql
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request:HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # request拦截处理
        # 对header 里面验证 jwt信息
        # django.core.handlers.wsgi.WSGIRequest
        from django.core.handlers.wsgi import WSGIRequest
        print(request, type(request), '~~~~~~~~~~~')
        addr = request.META.get('REMOTE_ADDR') # 不一定外网的浏览器端地址了，所以前面的服务上配置，让remoteaddr穿透过来
        # 访问redis，读取当前值 + 1，写回redis就可以了
        self.address[addr] = self.address.get(addr, 0) + 1

        if True:

            response = self.get_response(request) # view，去下一个中间件或者view

        # Code to be executed for each request/response after
        # the view is called.
        # response拦截处理

            return response
        else:
            return HttpResponse(status=401)



def authenticate(viewfunc):
    def wrapper(request:HttpRequest):
        # 认证检测 "HTTP_JWT"
        try:
            auth = request.META["HTTP_JWT"]
            payload = jwt.decode(auth, settings.SECRET_KEY, algorithms=[settings.ALG])# 篡改，过期
            print(payload, '~~~~~~~~~~~~~~~~~~')
            print(datetime.datetime.now().timestamp(), '~~~~~~~~~~~~~~')
            user = User.objects.get(pk=payload['user_id'])  # 以后要注意查询条件

            request.user = user

        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        ret = viewfunc(request)
        return ret

    return wrapper

@authenticate # test就是view函数，authentication验证用户身份，如果不通过，返回401，通过则调用test
def test(request): # 调用到test，说明认证通过

    return HttpResponse('test ok')



