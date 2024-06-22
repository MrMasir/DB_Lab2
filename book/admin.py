from django.contrib import admin
from .models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule

'''
# 创建每天执行一次的定时任务
schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.DAYS)
PeriodicTask.objects.create(interval=schedule, task='book.tasks.send_reminder_return_email', name='test')
'''
# Register your models here.
class BorrowsAdmin(admin.ModelAdmin):  #用于配置Borrows模型在管理后台的展示方式和行为
    list_display = ['bname', 'uname', 'return_date', 'borrow_date', 'status']
    list_filter = ['uname', 'bname']
    search_fields = ['uname', 'bname']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['bname', 'uname']
    list_filter = ['bname', 'uname']
    search_fields = ['bname', 'uname']

admin.site.register(BookInfo)
admin.site.register(UserInfo)
admin.site.register(BorrowInfo, BorrowsAdmin)
admin.site.register(ReservationInfo, ReservationAdmin)
#admin.site.register(MessageInfo)

