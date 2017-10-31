from django.shortcuts import render,render_to_response
from app01 import models
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django_comments.models import Comment

import django.db.models as models1
from django.contrib.auth.models import User


def Register(request):
    return render_to_response('register.html')

def acc_register(request):
    new_username = request.POST.get('username')
    new_password = request.POST.get('password')

    found = False
    if User.objects.filter(username=new_username).count():
        found = True
    else:
        found = False

    if found:
        return render_to_response('register.html', {'register_err': 'Username already exists'})

    else:

        new_user = User.objects.create_user(
            username=new_username,
            password=new_password
        )

        new_user.save()

        user = auth.authenticate(username=new_username,
                                 password=new_password
                                 )

        auth.login(request, user)

        return HttpResponseRedirect('/')


def acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/')
    else:
        return render_to_response('login.html',{'login_err':'Wrong username or password!'})

def Login(request):
    return render_to_response('login.html')

def logout_view(request):
    user = request.user
    auth.logout(request)
    return HttpResponse("<b>%s</b> logged out! <br/><a href='/login/'>Re-login</a>" % user)

def index(request):
    bbs_list = models.BBS.objects.all()
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'user':request.user,
                                            'bbs_category':bbs_categories,
                                            'cata_id': 0})

def category(request,cata_id):
    bbs_list=models.BBS.objects.filter(category__id=cata_id)
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'user':request.user,
                                            'bbs_category':bbs_categories,
                                            'cata_id':int(cata_id)})

def bbs_detail(request,bbs_id):
    bbs=models.BBS.objects.get(id=bbs_id)
    return render_to_response('bbs_detail.html',{'bbs_obj':bbs,'user':request.user,})

def sub_comment(request):
    bbs_id = request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')
    Comment.objects.create(
        content_type_id=12,  # bbs表在数据库中的id号
        object_pk=bbs_id,
        site_id=1,
        user=request.user,
        comment=comment,
    )
    return HttpResponseRedirect('/detail/%s'% bbs_id)

def bbs_pub(request):
    return render_to_response('bbs_pub.html',{  'user':request.user})

def bbs_sub(request):

    title = request.POST.get('title')
    category=request.POST.get('category')
    content = request.POST.get('content')
    summary = request.POST.get('summary')
    author = models.BBS_user.objects.get(user__username=request.user)
    models.BBS.objects.create(
        title=title,
        summary=summary,
        content=content,
        author=author,
        category_id=category,
        view_count=1,
        ranking=1,
       created_at=models1.DateTimeField(auto_now_add=True),  # 创建日期
    #    updated_at=models1.DateTimeField(auto_now_add=True),
    )
    return HttpResponse("<h2>Bbs was published, please enter <br/><a href='/'>return</a> to index!<h2>")