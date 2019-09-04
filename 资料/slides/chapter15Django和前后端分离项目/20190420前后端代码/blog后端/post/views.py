from django.shortcuts import render
from .models import Post, Content
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from user.views import authenticate
import simplejson
import datetime
from user.models import User
from django.db import transaction
import math


@authenticate # 会把httprequest header中的jwt提取出来验证，通过，说明此用户允许登录且已经登录了
def pub(request:HttpRequest): # 需要认证？
    # 已经成功验证了用户身份，只需要提交pub post
    post = Post()
    content = Content()

    try:
        payload = simplejson.loads(request.body)

        title = payload['title']
        text = payload['content']

        post.title = title
        post.postdate = datetime.datetime.now()
        #post.author = request.user
        post.author = User(id=request.user.id)

        with transaction.atomic():
            post.save() # save成功有post.id。save会自动提交

            content.content = text
            content.post = post
            #raise Exception()
            content.save() # 自动提交

        return JsonResponse({
            'post_id':post.id
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def get(request:HttpRequest, id): # /post/123 # 详情页
    print(id, '~~~~~~~~~~~~~~~~~~~~~~~~')
    try:
        id = int(id)
        post = Post.objects.get(pk=id)

        return JsonResponse({
            'post':{
                'post_id':post.id,
                'title':post.title,
                'postdate':post.postdate,
                'author':post.author.name,
                'author_id':post.author.id,
                #'author_id':post.author_id,
                'content':post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()


def validate(d:dict, name:str, default, convert_func, validate_func):
    try:
        result = convert_func(d.get(name, default))
        #result = result if result > 0 else default
        result = validate_func(result, default)
    except:
        result = default
    return result



def getall(request:HttpRequest): # /post/
    # 分页实现
    page = validate(request.GET, 'page', 1, int, lambda x,y: x if x > 0 else y)
    size = validate(request.GET, 'size', 20, int, lambda x,y: x if x > 0 and x < 101 else y)

    # page, 当前页； size 页内条目数 ； pages 总页数 ； 总条目数 count
    # pagination

    try:
        start = (page-1) * size
        posts = Post.objects

        count = posts.count() # 总行数
        posts = posts.order_by('-pk')[start:start+size] # 列表页，没有加用户 /post/?userid=4 /post/user/4

        return JsonResponse({
            'posts':[
                {
                    'post_id':post.id, # /post/1  <a href=/post/123>新闻xyz</a>
                    'title':post.title
                } for post in posts
            ], 'pagination':{
                'page':page,
                'size':size,
                'count':count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()



