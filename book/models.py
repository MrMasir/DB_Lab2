from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class BookInfo(models.Model):
    bname = models.CharField(max_length=20, verbose_name='书名')
    author = models.CharField(default=None, max_length=40, verbose_name='作者')
    pub_data = models.DateField(default=0, verbose_name='出版日期')
    publish = models.CharField(default = None, max_length=20, verbose_name='出版社')
    book_type = models.CharField(default= None, max_length = 20, verbose_name='书籍分类')
    bimage = models.ImageField(upload_to="userpic",null=True, blank=True,verbose_name='图片')
    #bstatus = models.BooleanField(default=True, verbose_name='借阅状态')

    def __str__(self):
        return self.bname

class UserInfo(models.Model):
    username = models.CharField(default=None,max_length=20, verbose_name='用户名', primary_key=True, blank = False)
    password = models.CharField(default=None, max_length=20, verbose_name='密码', blank = False)
    email = models.EmailField(default=None, verbose_name='邮箱', blank=False)
    headpic = models.ImageField(upload_to="userpic", null=True, blank=True)
    userphone = models.CharField(default=None ,max_length=11, verbose_name='电话')
    u_borrowed_num = models.IntegerField(default=0, verbose_name='借书数量')
    uprivilege = models.IntegerField(default=1, verbose_name='权限')

    def __str__(self):
        return self.username
    
class BorrowInfo(models.Model):
    bname = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='书籍名')
    uname = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='用户名')
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='借阅日期')
    return_date = models.DateTimeField(verbose_name='归还日期', null = True)
    status = models.BooleanField(default=False, verbose_name='借阅状态')

    def get_status(self):
        return self.status
    
class ReservationInfo(models.Model):
    bname = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='书籍名')
    uname = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='用户名')

   
    
class MessageInfo(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()

    def __str__(self):
        return self.title