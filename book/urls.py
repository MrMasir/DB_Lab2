from django.urls import re_path,path
from . import views
from django.contrib import admin

app_name = "library"

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^user_login/$', views.user_login, name="user_login"),
    re_path(r'^user/$', views.user, name="user"),
    re_path(r'^user_register/$', views.user_register, name="user_register"),
    re_path(r'^register_tools/$', views.register_tools, name="register_tools"),
    re_path(r'^login_tools/$', views.login_tools, name="login_tools"),
    re_path(r'^logout/$', views.logout, name="logout"),
    re_path(r'^user_info/$', views.user_info, name="user_info"),
    re_path(r'^user_info_update/(\w+)/$', views.user_info_update, name="user_info_update"),
    re_path(r'^querybook/$', views.querybook, name="querybook"),
    re_path(r'^book_info/(\d+)/$', views.book_info, name="book_info"),
    re_path(r'^borrow_info/$', views.borrow_info, name="borrow_info"),
    re_path(r'^edit/$', views.edit, name="edit"),
#    re_path(r'^active/(.*?)/$', views.active, name="active"),
    re_path(r'^messages/$', views.messages, name="messages"),
    re_path(r'^book_return/$', views.book_return, name="book_return"),
    re_path(r'^reserve_book/(\d+)/$', views.reserve_book, name="reserve_book"),
    re_path(r'^admin_login/$', views.admin_login, name="admin_login"),
    re_path(r'^admin_user/$', views.admin_user, name="admin_user"),
    re_path(r'^admin_book/$', views.admin_book, name="admin_book"),
    re_path(r'^admin_borrow/$', views.admin_borrow, name="admin_borrow"),
    re_path(r'^admin_reservation/$', views.admin_reservation, name="admin_reservation"),
    re_path(r'^admin_host/$', views.admin_host, name="admin_host"),
    re_path(r'^admin_book_edit/(\d+)$', views.admin_book_edit, name="admin_book_edit"),
    re_path(r'^admin_book_add$', views.admin_book_add, name="admin_book_add"),
    re_path(r'^admin_borrow_delete/(\d+)$', views.admin_borrow_delete, name="admin_borrow_delete"),
    re_path(r'^admin_reserve_delete/(\d+)$', views.admin_borrow_delete, name="admin_reserve_delete"),
    path('admin/', admin.site.urls),  # 添加管理员登录界面的路径
]