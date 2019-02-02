from django.conf.urls import url
from django.contrib import admin
from learn import views as calc_views
 
 
urlpatterns = [
    #url(r'^$', calc_views.home3, name='home'),
    url(r'^add/$', calc_views.add, name='add'),
    url(r'^admin/', admin.site.urls),
    url(r'^add/(\d+)/(\d+)/$', calc_views.old_add2_redirect),
    url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
    url(r'^$', calc_views.index, name='home'),
    url(r'^wechat/', calc_views.weixin_main, name='wechat'),
    url(r'^menu/', calc_views.create_menu, name='menu'),
]