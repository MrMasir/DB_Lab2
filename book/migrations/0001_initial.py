# Generated by Django 5.0.6 on 2024-06-12 17:51

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bname", models.CharField(max_length=20, verbose_name="书名")),
                (
                    "author",
                    models.CharField(default=None, max_length=40, verbose_name="作者"),
                ),
                ("pub_data", models.DateField(default=0, verbose_name="出版日期")),
                (
                    "publish",
                    models.CharField(default=None, max_length=20, verbose_name="出版社"),
                ),
                (
                    "book_type",
                    models.CharField(default=None, max_length=20, verbose_name="书籍分类"),
                ),
                (
                    "bimage",
                    models.ImageField(
                        blank=True, null=True, upload_to="userpic", verbose_name="图片"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MessageInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "username",
                    models.CharField(
                        default=None,
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                        verbose_name="用户名",
                    ),
                ),
                (
                    "password",
                    models.CharField(default=None, max_length=20, verbose_name="密码"),
                ),
                (
                    "email",
                    models.EmailField(default=None, max_length=254, verbose_name="邮箱"),
                ),
                (
                    "headpic",
                    models.ImageField(blank=True, null=True, upload_to="userpic"),
                ),
                (
                    "userphone",
                    models.CharField(default=None, max_length=11, verbose_name="电话"),
                ),
                ("u_borrowed_num", models.IntegerField(default=0, verbose_name="借书数量")),
                ("uprivilege", models.IntegerField(default=1, verbose_name="权限")),
            ],
        ),
        migrations.CreateModel(
            name="BorrowInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "borrow_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="借阅日期"),
                ),
                ("return_date", models.DateTimeField(verbose_name="归还日期")),
                ("status", models.BooleanField(default=False, verbose_name="借阅状态")),
                (
                    "bname",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book.bookinfo",
                        verbose_name="书籍名",
                    ),
                ),
                (
                    "uname",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户名",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReservationInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bname",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book.bookinfo",
                        verbose_name="书籍名",
                    ),
                ),
                (
                    "uname",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book.userinfo",
                        verbose_name="用户名",
                    ),
                ),
            ],
        ),
    ]
