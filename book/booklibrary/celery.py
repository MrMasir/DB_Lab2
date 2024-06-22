from __future__ import absolute_import
import os
from celery import Celery,platforms
from datetime import datetime
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booklibrary.settings')

app = Celery('booklibrary')
app.now = datetime.now
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#app.autodiscover_tasks(['book'], force=True)
'''
app.conf.beat_schedule = {
    'send-reminder-return-email': {
        'task': 'book.tasks.send_reminder_return_email',
        'schedule': crontab(hour=3, minute=1),
    },
}
'''

platforms.C_FORCE_ROOT = True

# 一个测试任务
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
