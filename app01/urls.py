from django.conf.urls import url
from django.contrib import admin
from app01 import views,urls
urlpatterns = [

    url(r'^$', views.index),
    url(r'^detail/([0-9]+)/$',views.bbs_detail),
    url(r'^sub_comment/$', views.sub_comment),
    url(r'^bbs_pub/$',views.bbs_pub),
    url(r'^bbs_sub/$', views.bbs_sub),
    url(r'^category/(\d+)/$', views.category),

]
