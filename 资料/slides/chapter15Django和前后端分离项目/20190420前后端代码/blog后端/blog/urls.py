"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import datetime

def index(request: HttpRequest):
    """视图函数：请求进来返回响应"""
    my_dict = {
        'a': ["{}*{}={}".format(i,j,i*j) for i in range(1, 10) for j in range(1, 10)],
        'b': 0,
        'c': list(range(1, 10)),
        'd': 'abc', 'date': datetime.datetime.now()
    }
    context = {'content': 'www.magedu.com', 'my_dict': my_dict}
    return render(request, 'index.html', context)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'', index),
    # url(r'^$', index),
    url(r'^index$', index),
    url(r'^user/', include('user.urls')), # user/*  user/reg  reg ; user/id/1  id/1
    url(r'^post/', include('post.urls')) # /post/1 GET
]
