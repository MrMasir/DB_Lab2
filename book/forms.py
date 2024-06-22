from django import forms
from .models import *

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'email', 'userphone']

class BookInfoForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        fields = ['bname', 'author', 'publish', 'pub_data', 'book_type', 'bimage']