from django.shortcuts import render, get_object_or_404, reverse #渲染模板、获取对象、反向解析URL
from django.http import HttpResponse, HttpResponseRedirect #返回http响应
from .models import *
from .forms import * #导入自定义用户表单
from datetime import * 
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired  #用于生成和验证安全令牌
from django.contrib import messages as Messages
from datetime import datetime, timedelta
from django.db import transaction

# Create your views here.

#主页视图
def index(request):
    username = request.session.get('username')
    if username:
        return render(request, 'booklibrary/index.html', {'username': username})
    else:
        return render(request, 'booklibrary/index.html')
    
#用户登录页面视图
def user_login(request):
    return render(request, 'booklibrary/user_login.html')

#用户详情视图
def user(request):
    uname = request.session["username"]
    if not uname:
        # 如果session中没有用户名，重定向到登录页面或者显示错误信息
        return render(request, "booklibrary/user_login.html", {"error": "用户未登录"})

    try:
        user = UserInfo.objects.get(username=uname)
    except UserInfo.DoesNotExist:
        # 用户不存在，显示错误信息或重定向到登录页面
        return render(request, "booklibrary/user_login.html", {"error": "请重新登录"})
    return render(request, 'booklibrary/user.html', {'user': user})

@transaction.atomic
#登录处理视图
def login_tools(request):
    users = UserInfo.objects.all()
    for user in users:
        if user.username == request.POST["username"]:
            if user.password == request.POST['pwd']:
                if user:
                    request.session["username"] = user.username
                    return HttpResponseRedirect(reverse("library:user"), {"user": user})
                else:
                    return render(request, "booklibrary/user_login.html", {"error": "账户未激活"})
            else:
                return render(request, "booklibrary/user_login.html", {"error": "密码错误，请重新输入"})
    else:
        return render(request, "booklibrary/user_login.html", {"error": "无该用户，请重新输入"})

#退出视图
def logout(request):
    request.session.clear()
    return render(request, "booklibrary/index.html")

#用户注册页面视图
def user_register(request):
    form = UserInfoForm()
    context = {
        "form":form
    }
    return render(request, "booklibrary/user_register.html",context)

@transaction.atomic
#注册处理视图
def register_tools(request):
    form = UserInfoForm(request.POST)
    # form.set_password(form.password)
    username = request.POST['username']
    if UserInfo.objects.filter(username=username).exists():
        message = "该用户名已被使用，请更换"
        context = {
            "form":form,
            "message":message
        }
        return render(request, "booklibrary/user_register.html", context)
    
    form.save()
    user = UserInfo.objects.get(username = username)
    user.password = user.password
    user.save()
    return render(request, "booklibrary/user_login.html")

#用户信息视图
def user_info(request):
    uname = request.session["username"]
    user = UserInfo.objects.get(username = uname)
    return render(request, "booklibrary/user_info.html",{"user":user})

@transaction.atomic
#用户信息更新视图
def user_info_update(request,id):
    user = UserInfo.objects.get(pk=id)
    if request.method == "GET":
        return render(request,"booklibrary/user_info_update.html",{"user":user})
    elif request.method == "POST":
        if len(request.POST["uname"]) == 0:
            user.username=user.username
        else:
            user.username = request.POST["uname"]
        if len(request.POST["pwd"]) == 0:
            user.password=user.password
        else:
            user.password = request.POST["pwd"]
        if request.FILES["headpic"]:
            user.headpic = request.FILES["headpic"]
        else:
            user.headpic = user.headpic
        if len(request.POST["email"]) == 0:
            user.email = user.email
        else:
            user.email = request.POST["email"]
        user.save()
        return render(request, "booklibrary/user_info.html", {"user": user})

#查询图书视图
def querybook(request):
    if request.method == "GET":
        return render(request,"booklibrary/querybook.html")
    elif request.method == "POST":
        item = request.POST["item"]
        query = request.POST["query"]
        if item == "bname":
            books = BookInfo.objects.all().filter(bname__contains = query)
        else:
            books = BookInfo.objects.all().filter(auther__contains = query)
        return render(request,"booklibrary/querybook.html",{"books":books})

@transaction.atomic
#图书详情视图
def book_info(request,id):
    if request.method == "GET":
        book = BookInfo.objects.get(pk = id)
        borrow = BorrowInfo.objects.all().filter(bname=book).filter(status=True).first()
        if borrow:
            res = True
        else:
            res = False
        return render(request, "booklibrary/book_info.html", {"book": book,"res":res,"borrow":borrow})
    elif request.method == "POST":
        book = BookInfo.objects.get(pk=id)
        uname = request.session["username"]
        user = UserInfo.objects.get(username=uname)

        borrows = BorrowInfo.objects.all().filter(uname=uname)
        for borrow in borrows:
            if borrow.return_date == None:
                borrow_date = borrow.borrow_date.date()
                now_datetime = datetime.now()
                if (borrow_date + timedelta(days=30) - now_datetime.date()).days <= 0:
                    user.uprivilege = 0

        if user.uprivilege == 0:
            if user.u_borrowed_num >= 3:
                Messages.error(request, "您的借书数量已达到上限，无法借书。")
                return HttpResponseRedirect("/book_info/" + str(book.id) + "/")
            else:
                Messages.error(request, "由于您借阅书籍逾期未归还，无法借书。")
                return HttpResponseRedirect("/book_info/" + str(book.id) + "/")
        
        borrows = BorrowInfo()
        borrows.uname = user
        borrows.bname = book
        borrows.status = True
        borrows.borrow_date = datetime.now()
        #borrows.return_date = datetime.now() + timedelta(days=30)
        borrows.return_date = None
        borrows.save()
        borrow = BorrowInfo.objects.all().filter(bname=book).filter(status=True)

        user.u_borrowed_num += 1
        if user.u_borrowed_num >= 3:
            user.uprivilege = 0
        user.save()

        return HttpResponseRedirect("/book_info/" + str(book.id) + "/", {"book": book,"res":True,"borrow":borrow})

#借阅信息视图
def borrow_info(request):
    uname = request.session["username"]
    user = UserInfo.objects.get(username=uname)
    borrows = BorrowInfo.objects.all().filter(uname=uname)
    return render(request, "booklibrary/borrow_info.html", {"borrows": borrows})

#留言视图
def edit(request):
    if request.method == "GET":
        return render(request,"booklibrary/edit.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        mes = MessageInfo(title=title,content=content)
        mes.save()
        return HttpResponseRedirect(reverse("library:index"))

#显示留言视图
def messages(request):
    return render(request,"booklibrary/message.html")

@transaction.atomic
#还书视图
def book_return(request):
    if request.method == "POST":
        borrow_id = request.POST["borrow_id"]   # 获取要归还的借阅记录ID
        try:
            borrow_info = BorrowInfo.objects.get(pk=borrow_id)
        except:
            return HttpResponse("Borrow record not found", status=404)
        # 将借阅状态设置为已归还
        if borrow_info.uname != request.session["username"]:
            return HttpResponse("未借阅该图书", status=403)
        borrow_info.status = False
        borrow_info.return_date = datetime.now()
        borrow_info.save()
        # 更新当前用户借书权限
        uname = request.session["username"]
        user = UserInfo.objects.get(username=uname)
        user.u_borrowed_num -= 1
        if user.uprivilege == 0:
            user.uprivilege = 1
        user.save()

        #向预约用户发送邮件
        reservations = ReservationInfo.objects.filter(bname=borrow_info.bname)

        for reservation in reservations:
            reserved_user = reservation.uname
            send_reminder_email(reserved_user.email, borrow_info.bname.bname)
            #删除预约记录
            reservation.delete()
        return HttpResponseRedirect('/borrow_info/')
    else:
        # 如果是 GET 请求，显示归还书籍的表单页面或相关信息
        return render(request, 'booklibrary/book_return.html')
    
def send_reminder_email(user_email, book_name):
    subject = '图书预约提醒'
    message = f'您预约的图书《{book_name}》现在可以借阅了。请尽快前往图书馆借阅。'
    from_email = 'masr18534612129@163.com'
    
    send_mail(subject, message, from_email, [user_email])

@transaction.atomic
# 用户预约视图
def reserve_book(request, id):
    if request.method == "POST":
        book = get_object_or_404(BookInfo, pk=id)
        uname = request.session.get("username")
        user = get_object_or_404(UserInfo, username=uname)

        # 创建预约信息
        reservation = ReservationInfo(
            uname=user,
            bname=book
        )
        reservation.save()

        # 添加成功预约的提示消息
        message = "预约成功！"
        borrow = BorrowInfo.objects.filter(bname=book, status=True).first()
        res = borrow is not None
        return render(request, "booklibrary/book_info.html", {"book": book, "res": res, "borrow": borrow, "message": message})
    
def admin_login(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_login.html")
    elif request.method == "POST":
        if request.POST["admin_name"] == "masiran" and request.POST["admin_pwd"] == "masiran":
            return render(request, "booklibrary/admin_host.html")
        else:
            return render(request, "booklibrary/admin_login.html", {"error": "用户名或密码错误"})

def admin_host(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_host.html")

@transaction.atomic     
def admin_user(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_user.html")
    elif request.method == "POST":
        query = request.POST["query"]
        users = UserInfo.objects.all().filter(username__contains = query)
        return render(request, "booklibrary/admin_user.html", {"users": users})

@transaction.atomic    
def admin_book(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_book.html")
    elif request.method == "POST":
        item = request.POST["item"]
        query = request.POST["query"]
        if item == "bname":
            books = BookInfo.objects.all().filter(bname__contains = query)
        else:
            books = BookInfo.objects.all().filter(author__contains = query)
        return render(request, "booklibrary/admin_book.html", {"books": books})
    
@transaction.atomic
def admin_borrow(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_borrow.html")
    elif request.method == "POST":
        item = request.POST["item"]
        query = request.POST["query"]
        if item == "bname":
            books = BookInfo.objects.all().filter(bname__contains = query)
            borrows = BorrowInfo.objects.all().filter(bname__in = books)
        elif item == "uname":
            users = UserInfo.objects.all().filter(username__contains = query)
            borrows = BorrowInfo.objects.all().filter(uname__in = users)
        else:
            borrows = []
        return render(request, "booklibrary/admin_borrow.html", {"borrows": borrows})

@transaction.atomic   
def admin_reservation(request):
    if request.method == "GET":
        return render(request, "booklibrary/admin_reservation.html")
    elif request.method == "POST":
        item = request.POST["item"]
        query = request.POST["query"]
        if item == "bname":
            books = BookInfo.objects.all().filter(bname__contains = query)
            reserves = ReservationInfo.objects.all().filter(bname__in = books)
        elif item == "uname":
            users = UserInfo.objects.all().filter(username__contains = query)
            reserves = ReservationInfo.objects.all().filter(uname__in = users)
        else:
            reserves = []
        return render(request, "booklibrary/admin_reservation.html", {"reserves": reserves})


@transaction.atomic
def admin_book_edit(request,id):
    book = BookInfo.objects.get(pk=id)
    if request.method == "GET":
        return render(request, "booklibrary/admin_book_edit.html", {"book": book})
    elif request.method == "POST":
        if 'delete' in request.POST:
            book.delete()
            return HttpResponseRedirect(reverse('library:admin_book'))
        
        if len(request.POST["bname"]) == 0:
            book.bname = book.bname
        else:
            book.bname = request.POST["bname"]
        if len(request.POST["author"]) == 0:
            book.author = book.author
        else:
            book.author = request.POST["author"]
        if len(request.POST["pub_data"]) == 0:
            book.pub_data = book.pub_data
        else:
            book.pub_data = request.POST["pub_data"]
        if len(request.POST["publish"]) == 0:
            book.publish = book.publish
        else:
            book.publish = request.POST["publish"]
        if len(request.POST["book_type"]) == 0:
            book.book_type = book.book_type
        else:
            book.book_type = request.POST["book_type"]
        if request.FILES["bimage"]:
            book.bimage = request.FILES["bimage"]
        else:
            book.bimage = book.bimage
        book.save()
        message = "已修改！"
        return HttpResponseRedirect(reverse("library:admin_book"))

@transaction.atomic 
def admin_book_add(request):
    if request.method == "GET":
        form = BookInfoForm()
        context = {
            "form":form
        }
        return render(request, "booklibrary/admin_book_add.html", context)
    elif request.method == "POST":
        form = BookInfoForm(request.POST, request.FILES)
        form.save()
        message = "添加成功！"
        return HttpResponseRedirect(reverse("library:admin_book"))

@transaction.atomic   
def admin_borrow_delete(request,id):
    borrow = BorrowInfo.objects.get(pk=id)
    borrow.delete()
    return HttpResponseRedirect(reverse("library:admin_borrow"))

@transaction.atomic
def admin_reserve_delete(request,id):
    reserve = ReservationInfo.objects.get(pk=id)
    reserve.delete()
    return HttpResponseRedirect(reverse("library:admin_reservation"))

    

