from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import BorrowInfo

@shared_task
def send_reminder_return_email():
    # 获取所有借阅记录
    borrow_infos = BorrowInfo.objects.all()
  
    for borrow_info in borrow_infos:
        # 获取当前日期和时间
        now_datetime = datetime.now()

# 将 borrow_date 转换为 datetime.date 类型
        borrow_date = borrow_info.borrow_date.date()
        # 计算距离截止日期的天数
        days_until_due = (borrow_date + timedelta(days=30) - now_datetime.date()).days
        if days_until_due <= 3:  # 在截止日期前3天发送提醒邮件
            # 发送邮件
            send_mail(
                '借书提醒',
                f'您借阅的图书《{borrow_info.bname}》将在{days_until_due}天后到期，请及时归还。',
                'masr18534612129@163.com',
                [borrow_info.uname.email],
                fail_silently=False,
            )

@shared_task
def add(x, y):
    return x+y
