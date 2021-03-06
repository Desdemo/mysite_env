from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               min_length=2,
                               max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='确认密码',
                               min_length=6,
                               max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == "":
            return ValidationError("新的昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': '请输入正确的邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                       'placeholder': '点击‘发送验证码’发送到邮箱'})
    )